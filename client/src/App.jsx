import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Button } from "./components/ui/button";
import "react-toastify/dist/ReactToastify.css";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Button>Click me</Button>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
