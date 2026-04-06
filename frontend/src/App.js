import React, { useState, useEffect } from "react";
import "./App.css";
import Papa from "papaparse"; // this is for parsing csv files, will probably find method later to just convert into json
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import ListingsGrid from "./components/ListingsGrid";
import Modal from "./components/Modal"

// Image stays in src so webpack handles it
import WahuImg from "./images/Wahu.webp";

function App() {
  const [collapsed, setCollapsed] = useState(false);
  const [listings, setListings] = useState([]);
  const [filters, setFilters] = useState({ search: "", beds: "", baths: "" });
  const [debouncedFilters, setDebouncedFilters] = useState(filters);
  const [selectedListing, setSelectedListing] = useState(null);

  // DEBOUNCING EFFECTS FOR SEARCHING
useEffect(() => {
  const timer = setTimeout(() => {
    setDebouncedFilters(filters);
  }, 200); // 200ms delay after last keystroke

  return () => clearTimeout(timer); // cancel if user keeps typing
}, [filters]);

  useEffect(() => {
    fetch("/data/umn_apartment_data.csv")
      .then((res) => res.text())
      .then((csvText) => {
        Papa.parse(csvText, {
          header: true,
          skipEmptyLines: true,
          complete: (results) => {
            const grouped = {};
            results.data.forEach((row) => {
              const building = row["Building Name"];
              if (!grouped[building]) {
                grouped[building] = {
                  title: building,
                  address: row["Address"],
                  image: WahuImg,
                  url: row["URL"],
                  amenities: row["Amenities"]
                    ? row["Amenities"].split(",").map(a => a.trim())
                    : [],
                  units: {},
                };
              }

              const unitKey = `${row["Beds"]}-${row["Baths"]}`;
              const rent = parseFloat(row["Rent"].replace(/[$,]/g, ""));
              const sqft = parseFloat(row["Sqft"]);         // ← no || 0

              if (!grouped[building].units[unitKey]) {
                grouped[building].units[unitKey] = {
                  beds: row["Beds"],
                  baths: row["Baths"],
                  minSqft: sqft || null,                    // ← null if missing
                  maxSqft: sqft || null,
                  minRent: rent,
                  maxRent: rent,
                  availability: row["Availability"],
                };
              } else {
                if (sqft) {                                 // ← only update if valid
                  const u = grouped[building].units[unitKey];
                  u.minSqft = u.minSqft ? Math.min(u.minSqft, sqft) : sqft;
                  u.maxSqft = u.maxSqft ? Math.max(u.maxSqft, sqft) : sqft;
                }
                grouped[building].units[unitKey].minRent = Math.min(grouped[building].units[unitKey].minRent, rent);
                grouped[building].units[unitKey].maxRent = Math.max(grouped[building].units[unitKey].maxRent, rent);
              }
            });

            const listings = Object.values(grouped).map((building) => ({
              ...building,
              units: Object.values(building.units).map((unit) => ({
                ...unit,
                sqft: !unit.minSqft                        // ← handle null
                  ? "N/A"
                  : unit.minSqft === unit.maxSqft
                    ? `${unit.minSqft}`
                    : `${unit.minSqft} - ${unit.maxSqft}`,
                rent: unit.minRent === unit.maxRent
                  ? `$${unit.minRent.toLocaleString()}`
                  : `$${unit.minRent.toLocaleString()} - $${unit.maxRent.toLocaleString()}`,
              })),
            }));

            setListings(listings);
          },
        });
      });
  }, []);
const filteredListings = listings.filter((listing) => {
  const title = listing.title || "";
  const address = listing.address || "";

  const matchesSearch =
    title.toLowerCase().includes(debouncedFilters.search.toLowerCase()) ||
    address.toLowerCase().includes(debouncedFilters.search.toLowerCase());

  const matchesBeds = !debouncedFilters.beds || listing.units.some((u) => {
    if (debouncedFilters.beds === "3+") return parseInt(u.beds) >= 3;
    return u.beds === debouncedFilters.beds;
  });

  const matchesBaths = !debouncedFilters.baths || listing.units.some((u) => {
    if (debouncedFilters.baths === "3+") return parseInt(u.baths) >= 3;
    return u.baths === debouncedFilters.baths;
  });

  return matchesSearch && matchesBeds && matchesBaths;
});

  return (
    <div className="App">
      <Header collapsed={collapsed} onToggle={() => setCollapsed((c) => !c)} />
      <Sidebar
        collapsed={collapsed}
        onToggle={() => setCollapsed((c) => !c)}
        filters={filters}
        setFilters={setFilters}
      />
      <Modal listing={selectedListing} onClose={() => setSelectedListing(null)} />
      <ListingsGrid
        collapsed={collapsed}
        listings={filteredListings}
        filters={debouncedFilters}
        onCardClick={setSelectedListing}
      />
    </div>
  );
}

export default App;
