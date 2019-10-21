// eslint-disable-next-line
import {InMemoryCache} from 'apollo-cache-inmemory/lib/index'
import {HttpLink} from 'apollo-link-http/lib/index'
import {ApolloClient} from 'apollo-client/index'
import fetch from 'unfetch'
// eslint-disable-next-line
import {IntrospectionFragmentMatcher} from 'apollo-cache-inmemory'
import introspectionQueryResultData from './fragmentTypes.json'

const fragmentMatcher = new IntrospectionFragmentMatcher({
  introspectionQueryResultData
})

const httpLink = new HttpLink({
  uri: process.env.NODE_ENV !== 'production' ? 'http://localhost:8000/api/graphql/' : '/api/graphql/',
  credentials: 'include',
  fetch: fetch,
  headers: {
    'X-CSRFToken': document.cookie.replace(/(?:(?:^|.*;\s*)csrftoken\s*=\s*([^;]*).*$)|^.*$/, '$1')
  }
})


// Create the apollo client
export default new ApolloClient({
  link: httpLink,
  cache: new InMemoryCache({fragmentMatcher}),
  connectToDevTools: true
})
