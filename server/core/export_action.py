# Created on 3/28/17 by maersu
import datetime
from django.contrib.admin.utils import lookup_field
from django.contrib.contenttypes.models import ContentType

from django.core.exceptions import PermissionDenied
from django.db.models import ManyToManyField
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.encoding import smart_str
from django.utils.html import strip_tags
from django.contrib import messages
from django.utils.text import slugify
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from django.conf import settings
import numbers

EXPORT_RECORDS_LIMIT = 5000

import logging

logger = logging.getLogger(__name__)


def primitive_value(value):
    if isinstance(value, numbers.Real) or isinstance(value, datetime.datetime) or isinstance(value,
                                                                                             datetime.date):
        return value

    if isinstance(value, list):
        return ','.join([smart_str(strip_tags(v)).strip() for v in value])

    val = smart_str(strip_tags(value)).strip()
    return val if val != 'None' else ''


def get_value(obj, field, modeladmin, keep_type=False):
    if '__' in field:
        # field is a related object. Start recursion.
        s = field.split('__')

        # check if obj is a dict or a object
        if isinstance(obj, dict):
            next_obj = obj.get(s[0], None)
        else:
            next_obj = getattr(obj, s[0], None)

        return get_value(next_obj, '__'.join(s[1:]), modeladmin)
    else:
        val = ''
        try:
            val = lookup_field(field, obj, modeladmin)
            if isinstance(val[0], ManyToManyField):
                val = '; '.join([u'%s' % a for a in val[-1].all()])
            else:
                val = val[-1]
        except Exception as e:
            attr = getattr(obj, field, None)
            try:
                if callable(attr):
                    val = attr()
                elif isinstance(obj, dict):
                    val = obj.get(field, None)
                else:
                    logger.warning('Field not found: {} from {}'.format(field, obj))
            except Exception as e:
                logger.exception('Not able to extract for {}'.format(field))
                return val

        if keep_type:
            return val

        return primitive_value(val)


def beautify_title(text):
    return text.replace('__', ' ').replace('_', ' ').replace('-', ' ').capitalize()


def export_as_excel(modeladmin, request, queryset):
    """
    Generic xls export admin action.
    """
    if queryset.count() > EXPORT_RECORDS_LIMIT:
        messages.error(request,
                       "Can't export more than {} records in one go. Narrow down your criteria using filters or search".format(
                           EXPORT_RECORDS_LIMIT))
        return HttpResponseRedirect(request.path_info)

    if not request.user.is_staff:
        raise PermissionDenied

    export_flatten_fields = []
    if hasattr(modeladmin, 'export_flatten_fields'):
        export_flatten_fields = modeladmin.export_flatten_fields

    if hasattr(modeladmin, 'export_fields_only'):
        fields = modeladmin.export_fields_only
    else:
        export_ignore_fields = (
                                   modeladmin.export_ignore_fields if hasattr(modeladmin,
                                                                              'export_ignore_fields') else []
                               ) + export_flatten_fields

        fields = [f.name for f in modeladmin.model._meta.get_fields() if f.name and f.name not in export_ignore_fields]

    if hasattr(modeladmin, 'export_extra_fields'):
        fields += modeladmin.export_extra_fields

    if hasattr(modeladmin, 'beautify_title'):
        _beautify_title = modeladmin.beautify_title
    else:
        _beautify_title = beautify_title

    flatten_keys = []

    if export_flatten_fields:
        for obj in queryset:
            for f in export_flatten_fields:
                d = get_value(obj, f, modeladmin, keep_type=True)
                flatten_keys += [k for k in d.keys() if k not in flatten_keys]

    has_absolute_url = hasattr(modeladmin.model, 'get_absolute_url')
    extra_urls = (['web url'] if has_absolute_url else []) + ['admin url']

    content_type = ContentType.objects.get_for_model(modeladmin.model)

    wb = Workbook()
    ws0 = wb.worksheets[0]
    ws0.title = modeladmin.model.__name__

    # write header row
    ws0.append([_beautify_title(f) for f in fields + flatten_keys + extra_urls])

    # Write data rows
    for obj in queryset:
        values = [get_value(obj, field, modeladmin) for field in fields]

        for field in export_flatten_fields:
            d = get_value(obj, field, modeladmin, keep_type=True)
            for k in flatten_keys:
                values.append(primitive_value(d.get(k)))

        if has_absolute_url:
            values.append('%s%s' % (settings.BASE_URL, obj.get_absolute_url()))

        values.append('%s%s' % (settings.BASE_URL,
                                reverse("admin:{}_{}_change".format(content_type.app_label, content_type.model),
                                        args=(obj.id,))))
        ws0.append(values)

    for extra in getattr(modeladmin, 'export_extra_sheets', []):
        f = getattr(modeladmin, extra)
        ws_extra = wb.create_sheet(title=getattr(f, 'sheet_title', extra))

        sheet_header = getattr(f, 'sheet_header', None)
        if sheet_header:
            ws_extra.append(sheet_header)

        for obj in queryset:
            for r in f(obj):
                if r:
                    ws_extra.append(r)

    file_name = slugify(
        '{}-export-{}'.format(ws0.title, datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S'))) + '.xlsx'

    response = HttpResponse(save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
    return response


export_as_excel.short_description = "Export selected to Excel"
