import React from "react";

export default function Sidebar({ collapsed, onToggle, filters, setFilters }) {
  return (
    <aside className={`sidebar ${collapsed ? "collapsed" : "expanded"}`}>
      <div className="sidebar-toggle" onClick={onToggle}>
        <span className="toggle-icon">☰</span>
      </div>

      {!collapsed && (
        <div className="sidebar-content">
          <h2>Filters</h2>
          <input
            type="text"
            placeholder="Search area"
            value={filters.search}
            onChange={(e) => setFilters({ ...filters, search: e.target.value })}
          />
          <select
            value={filters.beds}
            onChange={(e) => setFilters({ ...filters, beds: e.target.value })}
          >
            <option value="">Beds</option>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3+">3+</option>
          </select>
          <select
            value={filters.baths}
            onChange={(e) => setFilters({ ...filters, baths: e.target.value })}
          >
            <option value="">Baths</option>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3+">3+</option>
          </select>
          <div className="checkbox">
            <input type="checkbox" id="sublease" />
            <label htmlFor="sublease">Sublease?</label>
          </div>
        </div>
      )}
    </aside>
  );
}