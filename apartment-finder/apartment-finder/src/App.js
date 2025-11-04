import React, { useMemo, useState } from "react";
import "./App.css";

import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import ListingsGrid from "./components/ListingsGrid";

// Image stays in src so webpack handles it
import WahuImg from "./Wahu.webp";

function App() {
  const [collapsed, setCollapsed] = useState(false);

  // Mock data (27 identical items like your current map)
  const listings = useMemo(
    () =>
      Array.from({ length: 27 }, () => ({
        title: "Wahu",
        details: "$1050/mo · Studio · 1 ba",
        image: WahuImg,
      })),
    []
  );

  return (
    <div className="App">
      <Header />

      <Sidebar
        collapsed={collapsed}
        onToggle={() => setCollapsed((c) => !c)}
      />

      <ListingsGrid collapsed={collapsed} listings={listings} />
    </div>
  );
}

export default App;
