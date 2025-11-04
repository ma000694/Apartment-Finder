import React from "react";

export default function Sidebar({ collapsed, onToggle }) {
  return (
    <aside className={`sidebar ${collapsed ? "collapsed" : "expanded"}`}>
      <div
        className="sidebar-toggle"
        onClick={onToggle}
        title={collapsed ? "Open sidebar" : "Close sidebar"}
      >
        <span className="toggle-icon">☰</span>
      </div>

      {!collapsed && (
        <div className="sidebar-content">
          <h2>Filters</h2>
          <input type="text" placeholder="Search area" />
          <select>
            <option>Beds</option>
            <option>Studio</option>
            <option>1</option>
            <option>2</option>
            <option>3+</option>
          </select>
          <select>
            <option>Baths</option>
            <option>1</option>
            <option>2</option>
            <option>3+</option>
          </select>
          <div className="checkbox">
            <input type="checkbox" id="sublease" />
            <label htmlFor="sublease">Sublease?</label>
          </div>
          <button>Search</button>
        </div>
      )}
    </aside>
  );
}
