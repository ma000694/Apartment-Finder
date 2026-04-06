import React from "react";
import Card from "./Card";

export default function ListingsGrid({ collapsed, listings, filters = { search: "", beds: "", baths: "" }, onCardClick }) {
  return (
    <main className={`main-content ${collapsed ? "collapsed" : ""}`}>
      <div className="grid">
        {listings.map((item, i) => (
          <Card
            key={`${filters.search}-${filters.beds}-${filters.baths}-${item.title}`}
            index={i}
            title={item.title}
            address={item.address}
            units={item.units}
            image={item.image}
            onClick={() => onCardClick(item)}
          />
        ))}
      </div>
    </main>
  );
}