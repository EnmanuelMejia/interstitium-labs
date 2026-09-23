export type Swap = { theirs: string; ours: string; href: string };
export type SchoolModule = {
  name: string;
  units: string[];
  href: string;
  hrefLabel: string;
  check: { q: string; choices: string[]; answer: number; why: string };
};

export const swaps: Swap[] = [
  { theirs: "Webucator HTML, CSS, and forms", ours: "MDN, then the page preview on the bench", href: "https://developer.mozilla.org/en-US/docs/Learn" },
  { theirs: "Bootstrap as the layout course", ours: "CSS flex and grid. Bootstrap is optional and MIT, not required", href: "https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout" },
  { theirs: "jQuery", ours: "The DOM. The library is not the path", href: "https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model" },
  { theirs: "Vue, then a separate React course", ours: "React’s own docs first. Vue’s docs are the open alternative, not a second bootcamp", href: "https://react.dev/learn" },
  { theirs: "Per Scholas MERN and Firebase", ours: "Node and React docs. Data is PostgreSQL on the bench, not a vendor console", href: "https://nodejs.org/docs/latest/api/" },
  { theirs: "Oracle SQL, PL/SQL, and APEX", ours: "PostgreSQL on the bench. Oracle’s exams stay on their catalog", href: "https://www.postgresql.org/docs/current/tutorial.html" },
  { theirs: "Python and Django as their slides", ours: "docs.python.org and the Django documentation", href: "https://docs.djangoproject.com/" },
  { theirs: "PHP as their course", ours: "The PHP manual", href: "https://www.php.net/manual/en/" },
  { theirs: "DevOps boot camp built on Chef", ours: "Ansible’s manual. Recipes are not required", href: "https://docs.ansible.com/" },
  { theirs: "Their CI tool of the week", ours: "A pipeline that fails closed. Woodpecker is one open runner", href: "https://woodpecker-ci.org/docs/intro" },
  { theirs: "Copilot, or a chat bot pasted into SQL", ours: "Noah. The model does not replace the manual or the test", href: "/muse" },
];

const check = (q: string, choices: string[], why: string) => ({ q, choices, answer: 0, why });

export const schoolModules: SchoolModule[] = [
  {
    name: "Markup",
    units: ["A page has a document, not a picture of a document. Headings are structure.", "Write it on the bench and run the preview. Their HTML course is not loaded here."],
    href: "https://developer.mozilla.org/en-US/docs/Web/HTML",
    hrefLabel: "MDN HTML",
    check: check("A heading element is for", ["the structure of the page", "making text bold", "a database row", "a pipeline stage"], "Structure first. Paint later."),
  },
  {
    name: "Layout",
    units: ["Flex and grid cover the layouts Bootstrap is often used to hide.", "If you add Bootstrap later, you still have to read its own docs. It is not this course."],
    href: "https://developer.mozilla.org/en-US/docs/Web/CSS",
    hrefLabel: "MDN CSS",
    check: check("The layout we require is", ["CSS, which you can explain", "a specific paid theme", "jQuery UI", "an APEX template"], "The manual is MDN."),
  },
  {
    name: "Behavior",
    units: ["JavaScript changes the document through the DOM.", "A framework comes after you can say what the code does without it."],
    href: "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
    hrefLabel: "MDN JavaScript",
    check: check("The DOM is", ["the browser’s tree of the document", "a server framework", "a SQL dialect", "an editor"], "React and Vue both sit on top of that tree."),
  },
  {
    name: "Forms",
    units: ["Check the field in the browser so the user gets a fast answer.", "Check it again on the server. The browser is not a trust boundary."],
    href: "https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/form",
    hrefLabel: "MDN forms",
    check: check("A form check that exists only in the browser", ["can be skipped by a client", "is enough for a password", "replaces the server", "is authentication"], "The server repeats the check."),
  },
  {
    name: "Interface",
    units: ["React’s learn track is the interface course. State stays in one place you can name.", "Vue is MIT and documented. It is a second interface, not a requirement, and not jQuery."],
    href: "https://react.dev/learn",
    hrefLabel: "React docs",
    check: check("We do not teach jQuery as the path because", ["the DOM manual is shorter than a second library", "jQuery is required for React", "the bench cannot show HTML", "SQL needs it"], "Learn the platform, then one interface."),
  },
  {
    name: "Service",
    units: ["Node serves the request. Express is one router, documented at expressjs.com, not a secret framework.", "Per Scholas uses MongoDB and Firebase. Mongo’s license is not OSI. Firebase is a vendor. The table you can run here is PostgreSQL."],
    href: "https://expressjs.com/",
    hrefLabel: "Express",
    check: check("The database on the bench is", ["PostgreSQL dialect, on readings", "Firebase", "Oracle APEX", "a spreadsheet"], "SELECT already runs. Joins wait until the statement stays honest."),
  },
  {
    name: "Python web",
    units: ["Python’s tutorial is the language. Django’s docs are the full-stack Python path.", "We do not reprint a Django syllabus. The tutorial there is the work."],
    href: "https://docs.djangoproject.com/en/stable/intro/",
    hrefLabel: "Django tutorial",
    check: check("Django’s authority is", ["the Django project documentation", "a slide deck we host", "PL/SQL", "the PHP manual"], "Match the manual to the framework."),
  },
  {
    name: "Delivery",
    units: ["Git is the record. A pipeline is green only if a failed test turns it red.", "Webucator’s boot camp spends a day on Chef. Ansible is the open tool we point at. Docker’s manual covers the image. Kubernetes is the Roads module."],
    href: "https://docs.ansible.com/ansible/latest/getting_started/index.html",
    hrefLabel: "Ansible",
    check: check("Chef is not the lab because", ["Ansible’s manual is the open configuration tool we use", "configuration does not matter", "containers replace git", "CI should always be green"], "The tool can change. The failing gate cannot."),
  },
];
