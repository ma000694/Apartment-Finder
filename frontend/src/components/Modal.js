import React from "react";
import SneakyGolem from "../images/sneaky golem.jpeg";

export default function Modal({ listing, onClose }) {
  if (!listing) return null;

  const placeholderRecommended = [
    { title: "Recommended A", address: "123 Sne St E", beds: 2, baths: 2, rent: "$900" },
    { title: "Recommended B", address: "456 Aky Ave SE", beds: 1, baths: 1, rent: "$700" },
    { title: "Recommended C", address: "789 Golem Blvd SE", beds: 3, baths: 2, rent: "$1,100" },
  ];

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>✕</button>

        <img src={listing.image} alt={listing.title} className="modal-main-image" />

        <div className="modal-content">
          <div className="modal-header">
            <h2>{listing.title}</h2>
            <a href={listing.url} target="_blank" rel="noopener noreferrer" className="modal-link">
              Apartment Website ↗
            </a>
          </div>

          <p className="modal-address">{listing.address}</p>

          <h3 className="modal-section-title">Available Units</h3>
          <div className="modal-units">
            {listing.units.map((unit, i) => (
              <div key={i} className="modal-unit-row">
                <span>{unit.beds}bd · {unit.baths}ba · {unit.sqft || "N/A"} sqft</span>
                <div className="modal-unit-right">
                  <span className="modal-rent">{unit.rent}</span>
                  <span className="modal-availability">{unit.availability}</span>
                </div>
              </div>
            ))}
          </div>

          {listing.amenities && listing.amenities.length > 0 && (
            <>
              <h3 className="modal-section-title">Amenities</h3>
              <div className="modal-amenities">
                {listing.amenities.map((a, i) => (
                  <span key={i} className="amenity-tag">{a}</span>
                ))}
              </div>
            </>
          )}

          <h3 className="modal-section-title">Similar Apartments:</h3>
            <div className="modal-recommended">
            {placeholderRecommended.map((rec, i) => (
                <div key={i} className="rec-card">
                <img src={SneakyGolem} alt="recommended" className="rec-image" />
                <div className="rec-info">
                    <p className="rec-title">{rec.title}</p>
                    <p className="rec-details">{rec.beds}bd · {rec.baths}ba · {rec.rent}</p>
                    <p className="rec-address">{rec.address}</p>
                </div>
                </div>
            ))}
            </div>
        </div>
      </div>
    </div>
  );
}