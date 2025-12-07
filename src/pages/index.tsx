import React from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import './home.css'; // Import the professional book styling

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary hero-professional')}>
      <div className="container">
        <div className="hero-content">
          <div className="book-cover">
            <div className="book-spine">
              <div className="book-title-area">
                <h1 className="book-title">{siteConfig.title}</h1>
                <div className="book-subtitle">{siteConfig.tagline}</div>
              </div>
              <div className="author-info">
                <div className="author-name">Quratulain</div>
                <div className="author-credentials">
                  <span className="credential">MSC | MBA</span>
                  <span className="credential-divider">•</span>
                  <span className="credential">Full Stack Developer</span>
                  <span className="credential-divider">•</span>
                  <span className="credential">AI Engineer</span>
                </div>
              </div>
            </div>
          </div>

          <div className="book-description">
            <p className="book-tagline">A comprehensive guide to Artificial Intelligence, Robotics, and Advanced Technologies</p>
            <div className="book-features">
              <div className="feature-item">
                <div className="feature-icon">🤖</div>
                <div className="feature-text">AI & Machine Learning</div>
              </div>
              <div className="feature-item">
                <div className="feature-icon">🦾</div>
                <div className="feature-text">Robotics & Automation</div>
              </div>
              <div className="feature-item">
                <div className="feature-icon">🧠</div>
                <div className="feature-text">Neural Networks</div>
              </div>
              <div className="feature-item">
                <div className="feature-icon">🔬</div>
                <div className="feature-text">Research & Innovation</div>
              </div>
            </div>
          </div>

          <div className="cta-section">
            <a href="/docs/introduction/physical-ai" className="button button--secondary button--lg button--cta">
              Start Reading
            </a>
          </div>
        </div>
      </div>
    </header>
  );
}

export default function Home(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="A comprehensive guide to Artificial Intelligence, Robotics, and Advanced Technologies by Quratulain - MSC | MBA, Full Stack Developer | AI Engineer">
      <HomepageHeader />
      <main>
        <section className="features-section">
          <div className="container">
            <div className="row">
              <div className="col col--4">
                <div className="feature-card">
                  <h3>Advanced AI Concepts</h3>
                  <p>Deep dive into cutting-edge artificial intelligence technologies and methodologies.</p>
                </div>
              </div>
              <div className="col col--4">
                <div className="feature-card">
                  <h3>Practical Applications</h3>
                  <p>Real-world examples and implementations of AI in robotics and automation.</p>
                </div>
              </div>
              <div className="col col--4">
                <div className="feature-card">
                  <h3>Expert Guidance</h3>
                  <p>Insights from industry professionals with extensive experience in AI development.</p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}