# Business Overview: Mono Electric Loyalty Program

The **Mono Electric** project is a customer engagement and loyalty platform designed to reward professionals and retailers for their commitment to the brand. By leveraging a Telegram-based interface, the program facilitates a seamless "Scan & Earn" experience.

## 🎯 Program Goals
- **Incentivize Loyalty**: Reward electricians and sellers for choosing and promoting Mono Electric products.
- **Direct Communication**: Establish a direct channel for announcements, promotions, and support.
- **Market Analytics**: Gain insights into product distribution and regional demand through geolocated data.

## 👥 User Roles

The platform distinguishes between two primary user categories:

| Role | Target Audience | Reward per Scan | Requirements |
| :--- | :--- | :--- | :--- |
| **Electrician** | Field professionals installing equipment. | **50 Points** | Registration, Phone, Location. |
| **Seller** | Retailers and shop owners. | **20 Points** | Registration, Phone, Location, **SmartUp ID**. |

## 💰 Points & Rewards System

1.  **Scanning**: Users find a promo code (scratch-off or QR) on Mono Electric packaging.
2.  **Earn**: Upon entering the code into the bot, points are instantly credited to their account.
3.  **Redeem**: Users browse an in-app catalog of gifts (tools, gadgets, merchandise).
4.  **Order Processing**:
    - `Pending`: Request received.
    - `Approved`: Preparation phase.
    - `Sent`: Dispatched for delivery.
    - `Completed`: User confirms receipt.

## 📍 Geographic Intelligence
During registration, users provide their live location. The system resolves this to the specific **Region (Viloyat)** and **District (Tuman)** of Uzbekistan. This allows administrators to:
- Filter top-performing regions.
- Target broadcasts to specific geographic areas.
- Analyze market penetration.

## 🛠 CRM & Administration
A robust Django Admin panel allows the Mono Electric team to:
- Generate bulk QR codes for production.
- Manage the gift catalog and redemption requests.
- Send mass broadcasts with rich media.
- Monitor real-time statistics and leaderboards.
