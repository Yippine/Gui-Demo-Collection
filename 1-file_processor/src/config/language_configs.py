LANGUAGE_CONFIGS = {
    "Python": {
        "exclude_dirs": [".git", ".vscode", "venv", "__pycache__", "build", "dist", "*.egg-info"],
        "exclude_files": ["*.pyc", "*.pyo", "*.pyd", ".DS_Store", "Thumbs.db"],
        "include_files": ["*.py", "requirements.txt", "setup.py", "README.md", "LICENSE"],
    },
    "JavaScript": {
        "exclude_dirs": ["node_modules", "bower_components", "dist", "build", ".git", ".vscode"],
        "exclude_files": ["*.min.js", "*.bundle.js", "*.map", "package-lock.json", "yarn.lock", ".DS_Store"],
        "include_files": ["*.js", "*.jsx", "*.ts", "*.tsx", "package.json", "webpack.config.js", "README.md"],
    },
    "Java": {
        "exclude_dirs": ["target", "build", ".gradle", ".mvn", ".git", ".idea"],
        "exclude_files": ["*.class", "*.jar", ".DS_Store", "Thumbs.db"],
        "include_files": ["*.java", "pom.xml", "build.gradle", "README.md", "LICENSE"],
    },
    "C#": {
        "exclude_dirs": ["bin", "obj", ".vs", "packages", ".git"],
        "exclude_files": ["*.exe", "*.dll", "*.pdb", ".DS_Store", "Thumbs.db"],
        "include_files": ["*.cs", "*.csproj", "*.sln", "App.config", "Web.config", "README.md"],
    },
    "Ruby": {
        "exclude_dirs": [".bundle", "vendor", "tmp", "log", ".git"],
        "exclude_files": ["*.gem", ".DS_Store", "Thumbs.db"],
        "include_files": ["*.rb", "Gemfile", "Rakefile", "config.ru", "README.md", "LICENSE"],
    },
    "Go": {
        "exclude_dirs": ["vendor", "bin", ".git"],
        "exclude_files": ["*.exe", "*.test", "*.prof", ".DS_Store"],
        "include_files": ["*.go", "go.mod", "go.sum", "README.md", "LICENSE"],
    },
    "PHP": {
        "exclude_dirs": ["vendor", "node_modules", ".git"],
        "exclude_files": [".DS_Store", "Thumbs.db"],
        "include_files": ["*.php", "composer.json", "composer.lock", ".htaccess", "README.md"],
    },
    "Swift": {
        "exclude_dirs": [".build", "Pods", ".git"],
        "exclude_files": ["*.swiftmodule", ".DS_Store"],
        "include_files": ["*.swift", "Package.swift", "Podfile", "README.md", "LICENSE"],
    },
    "Kotlin": {
        "exclude_dirs": ["build", ".gradle", ".idea", ".git"],
        "exclude_files": ["*.class", "*.jar", ".DS_Store"],
        "include_files": ["*.kt", "*.kts", "build.gradle", "settings.gradle", "README.md"],
    },
    "Rust": {
        "exclude_dirs": ["target", ".git"],
        "exclude_files": ["*.rlib", "*.rmeta", ".DS_Store"],
        "include_files": ["*.rs", "Cargo.toml", "Cargo.lock", "README.md", "LICENSE"],
    },
    "TypeScript": {
        "exclude_dirs": ["node_modules", "dist", ".git"],
        "exclude_files": ["*.js", "*.js.map", ".DS_Store"],
        "include_files": ["*.ts", "*.tsx", "tsconfig.json", "package.json", "README.md"],
    },
    "C++": {
        "exclude_dirs": ["build", "bin", ".git"],
        "exclude_files": ["*.o", "*.out", "*.exe", ".DS_Store"],
        "include_files": ["*.cpp", "*.hpp", "*.h", "CMakeLists.txt", "README.md"],
    },
}
