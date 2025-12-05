/**
 * Creating a sidebar enables you to:
 - Create an ordered group of docs
 - Render a sidebar in the docs side navigation
 - By default, Docusaurus generates a sidebar from the docs folder structure
 */

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Introduction',
      items: [
        'introduction/physical-ai',
        'introduction/humanoid-architecture',
      ],
    },
    {
      type: 'category',
      label: 'ROS 2 Fundamentals',
      items: [
        'ros2-fundamentals/ros2-fundamentals',
      ],
    },
    {
      type: 'category',
      label: 'Digital Twin Simulation',
      items: [
        'digital-twin-sim/digital-twin-sim',
      ],
    },
    {
      type: 'category',
      label: 'NVIDIA Isaac Platform',
      items: [
        'nvidia-isaac/nvidia-isaac',
      ],
    },
    {
      type: 'category',
      label: 'Vision-Language-Action for Humanoids',
      items: [
        'vla-humanoids/vla-humanoids',
      ],
    },
    {
      type: 'category',
      label: 'Capstone System Overview',
      items: [
        'capstone-overview/capstone-overview',
      ],
    },
    {
      type: 'category',
      label: 'Appendices',
      items: [
        'appendices/glossary',
        'appendices/references',
      ],
    },
  ],
};

export default sidebars;