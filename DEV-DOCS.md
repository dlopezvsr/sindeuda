## General technical information
### Important points:
- Categories are created manually and not with NLP.
- Accounts are created manually as well.

### **User prompt workflow:**

- When the user creates the prompt, the LLM will validate if the request is processed as GET or POST transactions 
i.e., user wants to know what is the most expensive charge in the month,
in contrast with adding an income or expense transaction to db.
- The information of the previous point will be used as a condition where the prompt will trated differently depending
on the type.

POST: 
- If the user wants to add a transaction, the next step is to parse the information according to the prompt, 
where the LLM identifies each part of the text entered by the user: description, amount, type (income/expense), account.
- The function mentioned on the prior point will return a parsed dict processed with the LLM that will query the DB
to obtain the account and category ID matching up the description.
- Once the IDs are obtained, and all the information is parsed, the transaction will be entered on the DB directly.

GET:
- The whole prompt will be sent to the DB using the LLM to retrieve information i.e., user wants the most recurrent
charge of the year, or the total income of the month, etc.
- Once the response is caught will be returned to the user.

