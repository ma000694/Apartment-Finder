import React from "react";

export default function Card({ title, details, image }) {
  return (
    <div className="card">
      <img src={image} alt={title} />
      <div className="info">
        <h3>{title}</h3>
        <p>{details}</p>
      </div>
    </div>
  );
}
