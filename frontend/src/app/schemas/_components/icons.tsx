import React from 'react';

export const FileIcon: React.FC = () => {
  return (
    <svg
      width="64"
      height="64"
      viewBox="0 0 64 64"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <rect
        x="8"
        y="8"
        width="48"
        height="56"
        rx="4"
        ry="4"
        fill="#E2E8F0"
        stroke="#CBD5E0"
        strokeWidth="2"
      />
      <path
        d="M16 8V16C16 17.1046 16.8954 18 18 18H28V8H16Z"
        fill="#CBD5E0"
      />
      <text
        x="50%"
        y="85%"
        fontSize="12"
        fill="#2D3748"
        textAnchor="middle"
        dominantBaseline="middle"
      >
        YAML
      </text>
    </svg>
  );
};

