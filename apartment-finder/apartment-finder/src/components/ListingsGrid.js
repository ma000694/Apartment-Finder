import React from "react";
import Card from "./Card";

export default function ListingsGrid({ collapsed, listings }) {
  return (
    <main className={`main-content ${collapsed ? "collapsed" : ""}`}>
      <div className="grid">
        {listings.map((item, i) => (
          <Card
            key={i}
            title={item.title}
            details={item.details}
            image={item.image}
          />
        ))}
      </div>
    </main>
  );
}
