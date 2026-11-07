/* Architectural illustrations: these controls never initiate transactions. */
(() => {
  'use strict';
  const root = document.querySelector('[data-atlas-scenario-active]');
  if (!root) return;
  const stories = {
    private: {
      code: 'PRIVATE VALUE / DAARX + L10N',
      heading: ['Prove the payment.', 'Keep the amount private.'],
      description: 'A valid spend should not require a public financial biography. Hidden amounts and full-chain membership proofs are designed to let the chain check validity without naming the earlier output.',
      labels: ['YOUR DECISION', 'SEALED AMOUNT', 'VALIDITY PROOF', 'PRIVATE PAYEE'],
      steps: ['You authorize a private spend.', 'A proof establishes validity while the amount stays sealed.', 'The recipient receives value on its native chain.'],
      href: '/daarx.html', link: 'Inside private capital'
    },
    authority: {
      code: 'BOUNDED AUTHORITY / OPEN',
      heading: ['Delegate the task.', 'Keep control of the budget.'],
      description: 'An agent can act for you without inheriting unlimited financial power. OPEN mandates carry per-transaction, epoch and lifetime limits through the ancestry. Fees consume the allowance too.',
      labels: ['PRINCIPAL', 'MANDATE + CAPS', 'ANCESTRY CHECK', 'AGENT + RECEIPT'],
      steps: ['A principal defines a mandate and its spending limits.', 'The action must fit every applicable ancestor budget.', 'Admitted Agent value acts use native HALO backing and committed records.'],
      href: '/open.html', link: 'Explore accountable authority'
    },
    service: {
      code: 'BONDED SERVICES / NEXUS + NXXXS',
      heading: ['Choose the work.', 'See what stands behind it.'],
      description: 'Relays, proofs and settlement services have a native economic role. A customer chooses a supported service and provider; collateral and evidence back defined obligations. Ordinary sibling transfers carry no automatic NXXXS toll.',
      labels: ['CUSTOMER', 'SERVICE + TERMS', 'EVIDENCE', 'CHOSEN PROVIDER'],
      steps: ['Choose a provider for work you actually need.', 'Native collateral backs the declared obligation.', 'Evidence and payment follow the supported service rules.'],
      href: '/nexus.html', link: 'Explore bonded services'
    }
  };
  const buttons = [...document.querySelectorAll('[data-atlas-scenario]')];
  buttons.forEach(button => button.addEventListener('click', () => {
    const key = button.dataset.atlasScenario, story = stories[key];
    if (!story) return;
    buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    root.dataset.atlasScenarioActive = key;
    root.querySelector('[data-atlas-scenario-code]').textContent = story.code;
    const title = root.querySelector('[data-atlas-scenario-heading]');
    title.replaceChildren(document.createTextNode(story.heading[0]), document.createElement('br'), document.createTextNode(story.heading[1]));
    root.querySelector('[data-atlas-scenario-description]').textContent = story.description;
    root.querySelectorAll('[data-atlas-flow-label]').forEach((node,i) => { node.textContent = story.labels[i]; });
    root.querySelectorAll('[data-atlas-flow-step]').forEach((node,i) => { node.textContent = story.steps[i]; });
    const link = root.querySelector('[data-atlas-scenario-link]');
    link.href = story.href;
    const arrow = document.createElement('span'); arrow.setAttribute('aria-hidden','true'); arrow.textContent = '↗';
    link.replaceChildren(document.createTextNode(story.link+' '), arrow);
  }));
})();
