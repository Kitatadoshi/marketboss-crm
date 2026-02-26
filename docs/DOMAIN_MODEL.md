# Domain Model (MVP)

## Entities

### Lead
- id
- source
- name
- contact
- status (new/contacted/qualified/lost)
- createdAt

### Deal
- id
- leadId
- stage (diagnostic/niche/economics/launch/scale/won/lost)
- budget
- riskProfile
- platform (wb/ozon/both)
- targetRevenue
- createdAt

### Task
- id
- dealId
- title
- owner
- dueDate
- priority
- status (todo/in_progress/done/blocked)

### MetricSnapshot
- id
- dealId
- date
- impressions
- clicks
- orders
- buyouts
- revenue
- grossProfit

## Relations
- Lead 1:N Deal
- Deal 1:N Task
- Deal 1:N MetricSnapshot
