# **Project: Generative AIs & Chatbots, for fun and profit**

The goal of this project is to make you practice in your favorite skills on this trendy technology: chatbots backed by generative AIs.

It's an open project, it is willing to be fun and profitable for your knowledge and skills, and to put the focus on these technologies, which will bring added value to your profile.

**TL;DR**: In teams of up to 3, build a chatbot prototype on a topic of your choice (e.g. student support, language learning, admin FAQ). Your app needs a working backend (min. 2 endpoints) and frontend (min. 3 pages), built with Node or Python + Vanilla JS or React. You must integrate a generative AI: either a local model via llama.cpp or a free-tier API like Groq or Gemini (see docs/llm-alternatives.md ). On top of the code, you submit written documents covering: how innovative your idea is (with research to back it up), how you designed and organized your work (diagrams + task tracking), and the data privacy and security implications of your product. Each team member must document their individual contribution and thinking process throughout the project. The final grading includes a **video presentation** where you pitch your idea, demo the running app, and walk through your code and decisions. The total is graded out of 28 but capped at 20 : you don't need to do everything, focus on what you do best. All GenAI usage must be logged in GenAI-log.docx and kept under 30% of your total submission.

## **Objectives and grading rubric**

You'll have to create a product prototype, it can be whatever you want, based on chatbots and GenAIs. Subject ideas:

- Chatbot to support students in their specialization,
- Chatbot to help beginners to learn a new language,
- Support Chatbot for administrative questions at school,
- Etc.

The following grading details show a potential grade of 28 points, to let you choose whatever you prefer to work on. Even if you gain more than 20, the final grade will be set back to 20 points.

#### **Innovation (4pts)**

The idea you will develop for this project will be graded on its innovative power:

- **Innovative, 4pts:** The idea is rare or totally new (no publication or company dealing with this idea),
- **Niche, 2pts:** There is at least one competitor, or one publication implementing that idea,
- **Trendy, 1pt:** there are several competitors (less or equal than 3)
- **Common, 0pt:** the idea is widely spread, and there are plenty of resources talking about how to implement it.

Of course, you'll have to show in what category you're pretending your project to be in, and why with some detailed and commented research.

### **Conception and organization (4pts)**

Break down the project into small tasks and show in what order you have planned and then worked on each task. The subsequent report should contain elements of software design and project management necessary to understand your trajectory on this project:

- 2pt: Conception of the software solution, using diagrams and relevant software architecture comments (we should understand your design)
- 1pt: Usage of a tool to organize yourself (github tasks, Trello etc.)
- 1pt: Feedbacks on your development self organization.

## **Realization & Technologies used (6pts)**

This project is a transdisciplinary project allowing to practice what you have learned this semester. You should be able to demonstrate some:

- Backend skills with one of:
  - Node
  - Python
  - Other (possible upon validation with the professor)
- Frontend skills in either:
  - Vanilla JS
  - ReactJS
  - Other (mobile devices, or other frameworks, ask professor)

#### Grading:

- Fully functional backend (at least 2 endpoints): 3 points
- Fully functional frontend (at least 3 pages): 3 points

#### **Generative AI integration (6 points)**

You should integrate one of:

- Embedded AI model (using llama.cpp, prototype provided)
- Calling Generative AI APIs of your choice (pay attention to the pricing to avoid surprises).

**Note:** Running a model locally requires decent hardware (RAM, CPU). If your machine struggles, several **free-tier API alternatives** are available : no credit card required for most. See docs/llm-alternatives.md for a full list with setup guidance.

This is a topic which has been uncovered during the 4th semester, but it's a good opportunity to discover it. Epita students are massively using ChatGPT and sibling solutions, we assume it will be interesting to understand the complexity of those tools, from a software developer perspective.

The provided demo relies on GPT4All ([https://www.npmjs.com/package/gpt4all\)](https://www.npmjs.com/package/gpt4all) which is a library allowing to run a LLM model locally on your computer.

You can find the prototype application here: <https://github.com/thomasbroussard/llm-integration>

The improvements rely on several factors:

- The model used of course, but locally we are quite limited due to the hardware, though you can try different ones (the tested model here is q4\_0-orca-mini-3b.gguf ). Models have to be at the gguf format, these are the ones loadable through llama.cpp, used itself behind the scenes by gpt4all.
- The initial system prompt, to setup the context of the chatbot, the number of tokens per message and in the context (the "memory" of the genAI).
- The good understanding of what is your objective, the more it is precise, the more the outcomes will be interesting.

There are also plenty of possibilities to evolve this demo application to integrate better the chatbot features with better user experience handling (formatting, look and feel, integration of code highlights, etc).

**Tip for the performance grading criterion (4pts):** switching between providers is easy since most use the OpenAI-compatible API format. Benchmarking 2–3 different models/providers and documenting the differences is a great way to score well here.

#### Grading:

- **Integration of a gen AI: 2 pts:** your ability to integrate a gen AI in your application,
- **Working on gen AI performances: 4 pts:** you'll have to demonstrate the different things you've tried to complete your objectives, not managing to achieve them completely will not mean a worse grade, we want to understand your efforts and methodology here

**Working on look and feel: 1pt,** improve the user experience while using this chatbot.

#### **Data privacy concerns (4 points)**

Study and submit your conclusions about the usability of your product regarding the data it stores / requires to work:

Expose the issues about data privacy in that kind of software: 2pt

Propose solutions (technical and legal) to solve the data privacy issues: 2pt

### **Software Security Concerns (4 points)**

Study and submit your work regarding how well your product is secured. It includes proper authentication and role management.

Authentication: 2 pts

Role management: 1 pt

Listing security threats and counter measures: 1 pt

## **Team Composition**

- Teams of **1 to 3 members** are allowed.
- Each member must document their **individual contribution** and **thinking process** in a dedicated section of the project report (see Collaboration Log below).
- Work must be distributed and traceable : graders should be able to tell who did what and why.

#### **Collaboration Log**

Each team member must maintain a running log of their contributions throughout the project. Include it in your submission as collaboration-log.md (or as a section in your main report), structured as follows:

| Member | Task           | Description                                                | Decisions Made                                                      | Date       |
|--------|----------------|------------------------------------------------------------|---------------------------------------------------------------------|------------|
| Alice  | Backend<br>API | Implemented the /chat<br>endpoint and prompt<br>templating | Chose streaming response<br>over single response for<br>better UX   | 10/03/2025 |
| Bob    | Frontend       | Built the chat UI in React                                 | Used useReducer instead<br>of useState to manage<br>message history | 12/03/2025 |

| Member | Task            | Description                                             | Decisions Made                                                     | Date       |
|--------|-----------------|---------------------------------------------------------|--------------------------------------------------------------------|------------|
| Carol  | GenAI<br>tuning | Tested 3 models on<br>OpenRouter,<br>documented results | Chose Llama 3.1 8B over<br>Mistral 7B based on<br>coherence scores | 14/03/2025 |

The goal is not just to show *what* was done, but *how each person thought through their part* : include dead ends, trade-offs, and reasoning, not just final results.

## **Video Presentation**

The final grading includes a **video presentation**. It should cover:

- **Pitch** : what problem your chatbot solves and why the idea is relevant
- **Live demo** : run the application and show it working end-to-end
- **Code walkthrough** : explain the key technical decisions (architecture, AI integration, security)
- **Team contributions** : each member briefly presents the part they owned and their thinking process

Each team member must speak on camera. The video should be between **5 and 10 minutes**. Upload it as an unlisted YouTube/Google Drive link or include it in your repository.

## **Deliverables**

The deliverables should contain:

- A quick summary report of the tasks you've accomplished and where we can find the corresponding work in your submission
- A collaboration-log.md detailing each member's contributions and reasoning (see above)
- A **video presentation** (5–10 min) covering pitch, demo, code walkthrough, and individual contributions
- A GitHub repository where you invite the professor as contributor (GitHub username: l**ostmart** ):
- For each written section (Innovation, Conception, Data Privacy, Security): a separate document named with its part identifier, e.g. A-innovation.docx

## **Specific Conditions**

- Teams of up to 3 members are allowed. Contribution must be individual and traceable : do not submit work you did not personally produce.
- You can share knowledge and solution ideas with other teams, but not copy-paste work across teams.
- Generative AIs are allowed, but with the following conditions:
  - Be transparent by citing GenAI when it has helped you in your written production or in your code.
  - Provide a log at this format in the document GenAI-log.docx . The goal for us is to understand at which point the tool has been used, for what kind of task.

| Date       | Task                   | Description<br>of AI Tool<br>Usage                                                                  | Output                                 | Integration                   | Rationale                                                                           | Challeng<br>and<br>Conside                                 |
|------------|------------------------|-----------------------------------------------------------------------------------------------------|----------------------------------------|-------------------------------|-------------------------------------------------------------------------------------|------------------------------------------------------------|
| 15/01/2024 | Generating<br>Ideas    | Used<br>ChatGPT to<br>generate<br>story ideas<br>based on a<br>prompt<br>about a<br>futuristic city | Generated<br>5 story<br>ideas          | Yes,<br>selected 1<br>idea    | Selected<br>the most<br>unique<br>idea that<br>matched<br>the<br>project<br>theme   | Ensured<br>ideas we<br>original a<br>too gene              |
| 05/02/2024 | Creating<br>Characters | Used<br>ChatGPT to<br>develop<br>character<br>backgrounds<br>and traits                             | Generated<br>character<br>descriptions | Yes,<br>integrated<br>details | Integrated<br>interesting<br>character<br>traits to<br>add depth<br>to the<br>story | Verified<br>characte<br>were not<br>clichéd o<br>stereotyp |

Use the gen AI at maximum **30%** of the total production in your submission.