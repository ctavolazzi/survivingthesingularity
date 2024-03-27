  import { BASE_URL } from './config';

  async function fetchAPI(endpoint, options = {}) {
    const res = await fetch(`${BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });
  
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
  
    return await res.json();
  }
  
  export function getArticles() {
    return fetchAPI('/articles');
  }
  
  export function getArticleDetails(id) {
    return fetchAPI(`/articles/${id}`);
  }

  export function getArticles(query) {
    return {"articles": [{"id": 1, "title": "Article 1", "content": "Content 1"}, {"id": 2, "title": "Article 2", "content": "Content 2"}]
    // return fetchAPI(`/articles?q=${encodeURIComponent(query)}`);
  }