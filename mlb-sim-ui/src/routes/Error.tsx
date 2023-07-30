import { useRouteError } from "react-router-dom";
import NavBar from "../components/NavBar";


export default function ErrorPage() {
  const error: unknown = useRouteError();
  console.error(error);

  return (
    <div>
    <NavBar></NavBar>
    <div id="error-page">
      <h1>Oops!</h1>
      <p>Sorry, an unexpected error has occurred.</p>
      <p>
        <i>{error.statusText || error.message}</i>
      </p>
    </div>
    </div>
  );
}