import React from "react";

export default function Header({ collapsed, onToggle }) {
  return (
    <main className={`main-header ${collapsed ? "collapsed" : "expanded"}`}>
      <header style={{ whiteSpace: "nowrap" }}>gopher listings.</header>
    </main>
  );
}