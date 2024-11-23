export default async function apiCall(
    url, { 
      method = "GET",
       body=undefined, 
       headers = {} 
      }) {
    try {
      const response = await fetch(url, {
        method,
        body,
        headers,
      });
      return await response.json();
    } catch (error) {
      Promise.reject(error);
    }
  }