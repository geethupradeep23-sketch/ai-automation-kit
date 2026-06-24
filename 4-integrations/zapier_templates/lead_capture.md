# Zapier Template: Lead Capture & Automation

## Overview
Capture leads from multiple sources and automatically create CRM records, send emails, and notify your team.

## Setup Steps

### 1. Trigger: Multiple Lead Sources
Connect one or more:
- **Form Submission** (Typeform, JotForm, Unbounce)
- **Email** (Gmail, Outlook)
- **LinkedIn** (LinkedIn Lead Gen)
- **API Webhook** (Custom forms)

### 2. Action 1: Create CRM Record
**App:** HubSpot or Salesforce
```
Field Mapping:
- Email → Contact Email
- Name → Contact Name
- Phone → Phone Number
- Company → Company Name
- Message → Notes
```

### 3. Action 2: Send Welcome Email
**App:** Gmail or SendGrid
```
To: {{contact_email}}
Subject: Welcome to {{company_name}}
Body: Personalized welcome email
```

### 4. Action 3: Create Calendar Event
**App:** Google Calendar
```
Event: Follow-up Call with {{contact_name}}
Date: Tomorrow at 2 PM
Guests: sales_team@company.com
```

### 5. Action 4: Send Slack Notification
**App:** Slack
```
Channel: #sales
Message: New lead: {{contact_name}} from {{company_name}}
```

## Testing
1. Submit a test form
2. Verify all actions executed
3. Check CRM, email, calendar, and Slack

## Troubleshooting
- Verify API credentials are correct
- Check field mappings match your system
- Enable task history in Zapier for debugging
