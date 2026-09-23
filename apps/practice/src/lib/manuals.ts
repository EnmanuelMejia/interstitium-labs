export type Manual = {
  id: string;
  group: "Editor" | "JVM" | "Data" | "Chain";
  name: string;
  href: string;
  holds: string;
  rtfm: string;
};

export const manuals: Manual[] = [
  { id: "vim", group: "Editor", name: "Vim", href: "https://vimhelp.org/", holds: "Modal editing. The help is inside the editor: :help.", rtfm: "If the mode is wrong, the manual is one colon away." },
  { id: "vi", group: "Editor", name: "vi", href: "https://pubs.opengroup.org/onlinepubs/9699919799/utilities/vi.html", holds: "The POSIX editor vim still contains.", rtfm: "vi is not a lesser vim. It is the spec." },
  { id: "neovim", group: "Editor", name: "Neovim", href: "https://neovim.io/doc/", holds: "A vim descendant with its own manual.", rtfm: "A plugin manager is not the documentation." },
  { id: "emacs", group: "Editor", name: "Emacs", href: "https://www.gnu.org/software/emacs/manual/html_node/emacs/", holds: "The GNU manual, including the tutorial.", rtfm: "C-h t is the tutorial. The thread is not." },
  { id: "helix", group: "Editor", name: "Helix", href: "https://docs.helix-editor.com/", holds: "A selection-first editor with a short manual.", rtfm: "Kakoune’s cousin still expects you to read." },
  { id: "nano", group: "Editor", name: "nano", href: "https://www.nano-editor.org/dist/latest/nano.html", holds: "The small editor. The shortcuts are on the screen and in the manual.", rtfm: "The two lines at the bottom are the manual you skipped." },
  { id: "vscode", group: "Editor", name: "VS Code", href: "https://code.visualstudio.com/docs", holds: "Microsoft’s editor docs. We do not ship their binary.", rtfm: "An extension that hides the command is not a substitute for the docs." },
  { id: "jetbrains", group: "Editor", name: "JetBrains", href: "https://www.jetbrains.com/help/", holds: "IntelliJ and the rest of the suite. Their help, not a copy.", rtfm: "The intention menu is not the language specification." },
  { id: "eclipse", group: "Editor", name: "Eclipse IDE", href: "https://help.eclipse.org/", holds: "The Eclipse platform help.", rtfm: "A workspace error usually names the manual page. Open it." },
  { id: "openjdk", group: "JVM", name: "OpenJDK", href: "https://openjdk.org/", holds: "The reference implementation.", rtfm: "The JEP is the change. The blog is the rumor." },
  { id: "temurin", group: "JVM", name: "Eclipse Temurin", href: "https://adoptium.net/docs/", holds: "A build of OpenJDK you can install.", rtfm: "Which JDK printed java -version is the first fact." },
  { id: "oracle-jdk", group: "JVM", name: "Oracle JDK", href: "https://docs.oracle.com/en/java/javase/21/", holds: "Oracle’s Java SE documentation for a current release.", rtfm: "The tutorial and the spec are different books. Know which one you opened." },
  { id: "postgres", group: "Data", name: "PostgreSQL", href: "https://www.postgresql.org/docs/current/sql.html", holds: "The SQL we point at when the bench refuses a statement.", rtfm: "The error string is the page title you have not opened." },
  { id: "sqlite", group: "Data", name: "SQLite", href: "https://www.sqlite.org/lang.html", holds: "A small SQL dialect with a complete language page.", rtfm: "If it is not in the syntax diagrams, it is not in SQLite." },
  { id: "wolfram", group: "Data", name: "Wolfram Language", href: "https://reference.wolfram.com/language/", holds: "The function reference. Mathematica certification is Wolfram’s exam, not ours.", rtfm: "The function page has the examples. Start there." },
  { id: "xrpl", group: "Chain", name: "XRPL", href: "https://xrpl.org/docs.html", holds: "Ripple’s public ledger docs for XRP Ledger development.", rtfm: "A price chart is not the transaction format." },
  { id: "ethereum", group: "Chain", name: "Ethereum", href: "https://ethereum.org/developers/docs/", holds: "Protocol and application docs.", rtfm: "The yellow paper and a tutorial are not the same length for a reason." },
  { id: "bitcoin", group: "Chain", name: "Bitcoin", href: "https://bitcoin.org/bitcoin.pdf", holds: "The original paper. Implementation docs live with the client you actually run.", rtfm: "Nine pages. Then the client manual, not a thread." },
];
