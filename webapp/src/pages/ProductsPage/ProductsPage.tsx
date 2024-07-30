import PageWrapper from "../PageWrapper";
import { useState, useEffect } from "react";
import { Product } from "../../components/interfaces";
import { getProducts } from "../ApiHelper";
import Spinner from "../../components/Spinner/Spinner";

const DATA_STATES = {
  waiting: "WAITING",
  loaded: "LOADED",
  error: "ERROR",
};

const ProductsPage = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loadingState, setLoadingState] = useState(DATA_STATES.waiting);

  const fetchProducts = async () => {
    setLoadingState(DATA_STATES.waiting);
    const { products, errorOccured } = await getProducts();
    setProducts(products);
    setLoadingState(errorOccured ? DATA_STATES.error : DATA_STATES.loaded);
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  let content;
  if (loadingState === DATA_STATES.waiting)
    content = (
      <div
        className="flex flex-row justify-center w-full pt-4"
        data-testid="loading-spinner-container"
      >
        <Spinner />
      </div>
    );
  else if (loadingState === DATA_STATES.loaded) {
    content = (
      <div
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 mt-10"
        data-testid="pipeline-container"
      >
        {products.map((product) => (
          <div
            key={product.ProductID}
            className="bg-gray-400 p-4 rounded-lg transition ease-in-out duration-300 hover:scale-105"
          >
            <img
              src={product.ProductPhotoURL}
              alt={product.ProductName}
              className="w-full h-52 object-cover mb-2 rounded-lg"
            />
            <div className="px-2 flex gap-2 items-baseline">
              <h2 className="text-xl">{product.ProductName}</h2>
              <p className="text-gray-600 text-sm">id: {product.ProductID}</p>
            </div>
          </div>
        ))}
      </div>
    );
  } else {
    content = (
      <div
        className="flex flex-row justify-center w-full pt-4 text-3xl font-bold text-white"
        data-testid="error-container"
      >
        An error occured fetching the data!
      </div>
    );
  }

  return <PageWrapper>{content}</PageWrapper>;
};

export default ProductsPage;
