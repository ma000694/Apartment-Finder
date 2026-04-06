export default function Card({ title, address, units, image, index, onClick }) {
  return (
<div className="card" style={{ animationDelay: `${index * 0.07}s` }} onClick={onClick}>
      <img src={image} alt={title} />
      <div className="info">
        <h3>{title}</h3>
        <p className="address">{address}</p>
        <div className="units">
          {units.map((unit, i) => (
            <div key={i} className="unit-row">
              <span>{unit.beds}bd · {unit.baths}ba · {unit.sqft || "N/A"} sqft</span>
              <span>{unit.rent}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}