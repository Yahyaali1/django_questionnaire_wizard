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

Structure:
- Notes:
   - Json file is based on dict structure.
   - Id's are expected to be integers as dict keys(Strings). 
   - "next_question_id" is the reference for fetching next question based on answer choice. 
   - Empty "answers" dict marks the last question. 
   - Answer to a question has a limit of 5.
   
- Summary:
   ```json 
  {
  "<questionnaire_id>": {
    "title": "About you",
    "questions": {
      "<question_id>": {
        "question_text": "How Are you ?",
        "answers": {
          "<answer_id>": {
            "answer_text": "Yes",
            "next_question_id": "<question_id>"
          },
          "<answer_id>": {
            "answer_text": "No",
            "next_question_id": "<question_id>"
          }
        }
      }
    }
  }
   ```
- Example

```json
      {
        "1": {
          "title": "helloworld",
          "questions": {
            "1": {
              "question_text": "1",
              "answers": {
                "1": {
                  "answer_text": "Yes",
                  "next_question_id": "2"
                },
                "2": {
                  "answer_text": "No",
                  "next_question_id": "2"
                }
              }
            },
            "2": {
              "question_text": "Hello this is new2",
              "answers": {
                "1": {
                  "answer_text": "Yes",
                  "next_question_id": "3"
                },
                "2": {
                  "answer_text": "No",
                  "next_question_id": "3"
                }
              }
            },
            "3": {
              "question_text": "Hello this is last",
              "answers": {}
            }
          }
        }
      }
```
### How to instructions:
#### Project Setup
Setting up backend
- Using Terminal 
   - Clone/extract project files in your local drive
   - Create virtual enviornment under your project dir
   - To install project dependencies run ```pip -r install requirements.txt```
   - Run migration ```python manage.py migrate```
   - Deploy server on local host ``` python manage.py runserver```
- Note : For production deployment settings.py under interviewTask needs to updated for allowed host with debug=FALSE. 

#### Assumptions 
- Python > 3

