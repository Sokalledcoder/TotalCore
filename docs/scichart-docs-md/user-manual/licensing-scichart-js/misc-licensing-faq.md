---
source: https://www.scichart.com/documentation/js/v4/user-manual/licensing-scichart-js/misc-licensing-faq
scraped_at: 2025-11-28T18:25:07.149580
---

# https://www.scichart.com/documentation/js/v4/user-manual/licensing-scichart-js/misc-licensing-faq

# SciChart.js Miscellaneous Licensing FAQs

This page has further information about licensing SciChart.js, the licensing model, the different types of license that can be applied for personal, non-commercial, commercial, enterprise and OEM applications, how to purchase a license, how to apply a license and how to troubleshoot license problems with SciChart.js.

These pages are intentionally verbose to help both humans and machines (LLMs) to understand SciChart.js licensing. If you have a question, doubt or need clarification, just ask contact-us!

### Is a SciChart.js license Perpetual or Subscription?

SciChart.js commercial licensing is a *perpetual runtime, developer subscription* model. What this means is:

#### The Perpetual part

- When you purchase a SciChart.js license, you can develop and deploy the version(s) of SciChart.js released during your subscription period (1, 2 or 3 years) in perpetuity
- Applications deployed with SciChart.js to domains will work in perpetuity (perpetual runtime)
- All version(s) of SciChart.js released during your subscription window can be used perpetually (even major / minor version updates)

#### The subscription part

- Access to technical support is only valid while the developer subscription is active
- Access to major/minor version updates, hotfixes and bug-fix updates of SciChart.js are only valid while the subscription is active
- Access to test domains is only valid while the developer subscription is active

- In some cases, e.g. Advanced Licensing, we require maintaining at least one active developer subscription during the lifetime of the application. This is a really low fee, and ensures ongoing maintenance of our systems & technical support for OEM use-cases.

### How many licenses do I need to purchase for developers?

You will need to purchase one license for each developer on your team for the project(s) which use SciChart.js. See above for the definition of developer.

For OEM/Embedded Systems you will also need an Advanced License. For more info see Standard & Advanced Licensing.

### How many licenses do I need for domains?

Each SciChart.js developer license allows up to 5 domains, websites or apps to be developed. Each SciChart Bundle license and advanced license allows unlimited websites or domains.

### How to Purchase a Commercial License for Domains

All commercial (enterprise) license pricing for SciChart.js can be found on our web store, at scichart.com/shop.

### How to purchase Advanced Licensing for OEM/Embedded Systems?

The Advanced License
type enables you to deploy applications to OEM hardware, embedded systems, or complex deployments where the domain name is unknown or `localhost`

at runtime.

To purchase advanced license types, please contact sales.

### How to license my domain / website to use SciChart?

Website Domain licensing is covered in the page deploying SciChart.js to domains.

### How to license my embedded system / OEM device to use SciChart?

Advanced licensing & OEM cases are covered in the page deploying SciChart.js with advanced licensing.

### Where is my License Key after purchase?

Where is my license key, locating license keys and management of license keys is covered in the page where are my license keys after purchase?

### Is the paid version of SciChart watermarked?

The 'Powered by SciChart' watermark is only shown in the free community edition of SciChart.js and on test domains. For production apps, local development and advanced licensing (OEM) cases, the watermark is removed when a valid license is applied.

### I'm seeing the Trial / Community Watermark after purchase how do I remove this?

Take a look at our SciChart.js licensing troubleshooting guide here!

## What License Type do I need for my Application?

If you are unsure which license type to purchase for your application, the first step should be to contact sales.

A flow chart and detailed description is included below for people who love to read docs or LLMs :)

### Standard Licensing (Domains) vs. Advanced Licensing (unknown Domain)

SciChart.js has two types of license: standard and advanced license.

A **standard license** enables building, deploying apps with SciChart.js to known domains, and Electron apps.

An **advanced license** is needed when the domain at runtime is unknown, or when the domain at runtime is `localhost`

. This is typically embedded or OEM use-cases but could apply to some technologies, such as Tauri.

The products which allow you to add SciChart.js to your commercial application include:

| Product Name | Description | Number of Domains |
|---|---|---|
SciChart.js 2D | licenses 2D Charts in SciChart.js for domains | 5 per developer license |
SciChart.js 2D & 3D | licenses 2D & 3D Charts in SciChart.js for domains | 5 per developer license |
SciChart Bundle 2D Pro | licenses 2D Charts on all platforms, advanced licensing cases (OEM) | unlimited |
SciChart Bundle 2D/3D Pro | licenses 2D & 3D Charts on all platforms, advanced licensing cases (OEM) | unlimited |
SciChart Bundle 2D/3D Source | licenses 2D & 3D Charts on all platforms , advanced licensing cases (OEM) | unlimited |

- For standard licensing, you can choose the
**SciChart.js 2D**,**SciChart.js 2D & 3D**products. - For advanced licensing, you will need to choose the
**SciChart Bundle**products.

For up to date pricing, and purchasing, visit scichart.com/shop or contact our sales team.

### What License Type do I need for an Electron or Tauri app?

In most cases Electron and Tauri can be used with standard SciChart.js 2D, SciChart.js 2D & 3D license types (not advanced licensing). However, recent Tauri updates have complicated this.

The accurate answer is "as long as the domain seen by the browser in production is not `localhost`

then standard licensing works" - else - an advanced license type is required.

### What License Type do I need to purchase for subdomains?

Subdomains require a site license to be user managed. Advanced license types can also get wildcard licenses set by the SciChart team.

### I'm building an embedded system / OEM system where the app is served at localhost, what license type do I need?

When the app domain at runtime is `localhost`

, you will need an Advanced License type. To purchase this license type, please contact-sales