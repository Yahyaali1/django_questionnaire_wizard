# django_questionnaire_wizard


## Project Approach 
- Provides Api for performing questionnaires.
- Quesionnaires can be added in quesitionnaires.json.
- Conversation is logged onto console as the questionnaire ends.

### Api 
- Fetch 
   - url: `` http://localhost:8000/questionnaire/fetch``
   - response: 
   ``` javascript
   [
    {
        "questionnaire_id": 1,
        "title": "helloworld"
    },
    {
        "questionnaire_id": 2,
        "title": "helloworld"
    }] 
    ```
- Submit
  - Returns first question under the given questionnaire id ``http://localhost:8000/questionnaire/submit/<questionnaire_id>`` 
  - Returns specific question under the given questionnaire id ``http://localhost:8000/questionnaire/submit/<questionnaire_id>/<question_id>``   
  - (Returns specific next question linked with answer id) ``http://localhost:8000/questionnaire/submit/<questionnaire_id>/<question_id>/<answer_id>`` 
  - Response structure:
  ```json
  {
  "question_text": "1",
  "answers": [
    {
      "answer_text": "Yes",
      "next_question_id": "2",
      "answer_id": "1"
    },
    {
      "answer_text": "No",
      "next_question_id": "2",
      "answer_id": "2"
    }
  ],
  "questionnaire_id": "1",
  "question_id": "1"
  }
  ```
  - Note: If the "answers" array is empty, it reflects that end of questionnaire has been reached. 
- Api Error 
  - Following error response structure is followed (errorCode: 404):
  ```json
    {"error": "No questionnaire found with this id"}
  ```
### Questionnaire Strcuture File

### How to instructions:
 

#### Assumptions 
- Python > 3

