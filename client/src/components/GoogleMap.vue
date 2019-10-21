<template>
  <div>
    <GmapMap
      v-if="coordinates"
      :center="{lat: coordinates[0].latitude, lng: coordinates[0].longitude}"
      :zoom="7"
      ref="mapRef"
      :options="options"
      style="width: 100%; height: 30vh; margin: 0 auto; background: white;"
    >
      <GmapMarker
        :key="index"
        v-for="(c, index) in coordinates"
        :position="{lat: c.latitude, lng: c.longitude}"
        :clickable="false"
        :draggable="true"
      />
    </GmapMap>
  </div>
</template>
<script>
  export default {
    name: 'google-map',
    props: ['coordinates'],
    data: function () {
      return {
        options: {
          mapTypeControl: false,
          scaleControl: false,
          streetViewControl: false,
          rotateControl: false,
          fullscreenControl: false
        }
      }
    },

    mounted() {
      if (this.coordinates.length === 0) {
        return
      }
      this.$refs.mapRef.$mapPromise.then((map) => {
        window.google.maps.event.addListenerOnce(map, 'idle', (event) => {
          var newZoom = map.getZoom()
          if ((newZoom > 13) || (typeof newZoom === 'undefined')) {
            newZoom = 13
          }
          map.setZoom(newZoom)
        })

        const bounds = new window.google.maps.LatLngBounds()
        for (let m of this.coordinates) {
          bounds.extend({lat: m.latitude, lng: m.longitude})
        }
        map.fitBounds(bounds)
      })
    }
  }
</script>
