# Categorized Skill Database for smarter recommendations

SKILL_CATEGORIES = {
    "Languages": {
        "python", "java", "c++", "c#", "javascript", "typescript", "ruby", "go", "golang", "swift", "kotlin", "php", "rust", "scala", "r", "matlab", "perl", "lua", "dart", "html", "css", "sql", "bash", "shell", "powershell"
    },
    "Frontend": {
        "react", "react.js", "angular", "vue", "vue.js", "next.js", "nuxt.js", "svelte", "jquery", "bootstrap", "tailwind", "express", "express.js", "django", "flask", "fastapi", "spring", "spring boot", "rails", "ruby on rails", "asp.net", "laravel", "symfony", "node.js", "nodejs"
    },
    "AI/ML": {
        "tensorflow", "keras", "pytorch", "scikit-learn", "sklearn", "pandas", "numpy", "matplotlib", "seaborn", "opencv", "nltk", "spacy", "spark", "hadoop", "tableau", "power bi", "jupyter", "xgboost", "lightgbm", "catboost", "hugging face", "transformers", "llm", "bert", "gpt", "nlp", "computer vision", "statistics", "probability"
    },
    "Database": {
        "postgresql", "postgres", "mysql", "sqlite", "mongodb", "cassandra", "redis", "elasticsearch", "dynamodb", "oracle", "mssql", "firebase", "firestore", "mariadb", "neo4j"
    },
    "DevOps & Cloud": {
        "aws", "amazon web services", "azure", "google cloud", "gcp", "docker", "kubernetes", "k8s", "jenkins", "gitlab ci", "github actions", "circleci", "travis ci", "terraform", "ansible", "chef", "puppet", "linux", "unix", "nginx", "apache", "heroku", "netlify", "vercel", "digitalocean", "lambda", "ec2", "s3"
    },
    "Tools": {
        "git", "github", "gitlab", "bitbucket", "jira", "confluence", "trello", "slack", "figma", "postman", "swagger", "vscode", "intellij", "pycharm", "eclipse", "xcode", "android studio"
    },
    "Concepts": {
        "agile", "scrum", "kanban", "rest", "restful", "graphql", "soap", "mvc", "mvvm", "microservices", "serverless", "oop", "functional programming", "tdt", "bdd", "ci/cd", "devops", "mlops", "system design", "distributed systems", "algorithms", "data structures"
    },
    "Soft Skills": {
        "leadership", "communication", "teamwork", "problem solving", "critical thinking", "adaptability", "mentoring", "management"
    }
}

# Flatten for NLP extraction
SKILL_DB = set().union(*SKILL_CATEGORIES.values())
