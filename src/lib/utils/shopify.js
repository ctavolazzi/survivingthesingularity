/**
 * Shopify Storefront API utilities
 *
 * This file contains functions for interacting with the Shopify Storefront API
 * to fetch products and other data from a Shopify store.
 */

// Replace these with your actual Shopify credentials
const SHOPIFY_DOMAIN = 'your-store.myshopify.com';
const STOREFRONT_ACCESS_TOKEN = 'your-storefront-access-token';

/**
 * Fetch a specific product by handle (slug)
 * @param {string} handle - The product handle/slug
 * @returns {Promise<Object>} - The product data
 */
export async function fetchProductByHandle(handle) {
  try {
    const response = await fetch(
      `https://${SHOPIFY_DOMAIN}/api/2023-10/graphql.json`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Shopify-Storefront-Access-Token': STOREFRONT_ACCESS_TOKEN,
        },
        body: JSON.stringify({
          query: `
            query getProductByHandle($handle: String!) {
              product(handle: $handle) {
                id
                title
                handle
                description
                priceRange {
                  minVariantPrice {
                    amount
                    currencyCode
                  }
                }
                images(first: 1) {
                  edges {
                    node {
                      url
                      altText
                    }
                  }
                }
              }
            }
          `,
          variables: {
            handle,
          },
        }),
      }
    );

    const { data } = await response.json();

    if (!data || !data.product) {
      console.error('Product not found');
      return null;
    }

    // Format the product data for our component
    const product = data.product;
    const price = product.priceRange.minVariantPrice.amount;
    const formattedPrice = parseFloat(price).toFixed(2);
    const image = product.images.edges.length > 0 ? product.images.edges[0].node.url : '';

    return {
      id: product.id,
      title: product.title,
      description: product.description,
      price: formattedPrice,
      image: image,
      url: `https://${SHOPIFY_DOMAIN}/products/${product.handle}`
    };
  } catch (error) {
    console.error('Error fetching product:', error);
    return null;
  }
}

/**
 * Fetch featured products
 * @param {number} limit - Number of products to fetch
 * @returns {Promise<Array>} - Array of featured products
 */
export async function fetchFeaturedProducts(limit = 3) {
  try {
    const response = await fetch(
      `https://${SHOPIFY_DOMAIN}/api/2023-10/graphql.json`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Shopify-Storefront-Access-Token': STOREFRONT_ACCESS_TOKEN,
        },
        body: JSON.stringify({
          query: `
            query getFeaturedProducts($limit: Int!) {
              products(first: $limit, sortKey: BEST_SELLING) {
                edges {
                  node {
                    id
                    title
                    handle
                    priceRange {
                      minVariantPrice {
                        amount
                        currencyCode
                      }
                    }
                    images(first: 1) {
                      edges {
                        node {
                          url
                          altText
                        }
                      }
                    }
                  }
                }
              }
            }
          `,
          variables: {
            limit,
          },
        }),
      }
    );

    const { data } = await response.json();

    if (!data || !data.products || !data.products.edges) {
      console.error('Products not found');
      return [];
    }

    // Format the product data for our component
    return data.products.edges.map(({ node: product }) => {
      const price = product.priceRange.minVariantPrice.amount;
      const formattedPrice = parseFloat(price).toFixed(2);
      const image = product.images.edges.length > 0 ? product.images.edges[0].node.url : '';

      return {
        id: product.id,
        title: product.title,
        price: formattedPrice,
        image: image,
        url: `https://${SHOPIFY_DOMAIN}/products/${product.handle}`
      };
    });
  } catch (error) {
    console.error('Error fetching products:', error);
    return [];
  }
}

/**
 * For development/preview only:
 * Returns a mock product when actual Shopify credentials aren't set up.
 */
export function getMockFeaturedProduct() {
  return {
    title: "Dragon's Eye Pendant",
    price: "59.99",
    image: "/images/treasure-tavern-square.png", // Fallback to use our logo as product image
    url: "https://treasuretavern.com/products/dragons-eye-pendant"
  };
}