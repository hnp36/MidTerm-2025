# Advanced Python Calculator  
A command-line calculator with a REPL interface, plugin system, history management using Pandas, professional logging, and design pattern implementations for scalability.

---

## 🔗 Repository Link
[🔗 GitHub Repository](https://github.com/hnp36/MidTerm-2025.git)

---

## 📌 Design Patterns Implemented

Our calculator follows key software design patterns to ensure scalability and maintainability:

### 1️⃣ Facade Pattern  
- Why? Simplifies interaction with complex functionalities, providing a clean API.  
- Where? The `Calculator` class acts as a Facade to arithmetic operations.  
- Implementation:  
  - Code: [`calculator/__init__.py`]
  - Example:  
    ```python
    class Calculator:
        @staticmethod
        def add_numbers(value1: Decimal, value2: Decimal) -> Decimal:
            return Calculator.execute_operation(value1, value2, addition)
    ```
  
### 2️⃣ Command Pattern  
- Why? Enables dynamically adding commands to the REPL without modifying core logic.  
- Where? The `CommandHandler` dynamically loads command plugins.  
- Implementation: 
  - Code: [`calculator/commands/command_handler.py`]
  - Example:  
    ```python
    def load_plugins(self):
        """Dynamically load command classes from the plugins folder."""
        package = calculator.plugins
        for _, module_name, _ in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
            module = importlib.import_module(module_name)
            for name, obj in vars(module).items():
                if isinstance(obj, type) and issubclass(obj, Command) and obj is not Command:
                    self.register_command(name.replace("Command", "").lower(), obj())
    ```

### 3️⃣ Singleton Pattern 
- Why? Ensures a single instance of the `HistoryManager` for managing calculation history.  
- Where? `history_manager.py`  
- Implementation: 
  - Code: [`history_manager.py`]
  - Example:  
    ```python
    class HistoryManager:
        _instance = None  # Singleton instance
        def __new__(cls, *args, **kwargs):
            if cls._instance is None:
                cls._instance = super(HistoryManager, cls).__new__(cls)
            return cls._instance
    ```

### 4️⃣ Factory Method Pattern  
- Why? Encapsulates object creation for `Calculation` instances.  
- Where? `Calculation.create()`  
- Implementation:  
  - Code: [`calculator/calculation.py`]
  - Example:  
    ```python
    @staticmethod
    def create(value1: Decimal, value2: Decimal, operation: Callable[[Decimal, Decimal], Decimal]):
        return Calculation(value1, value2, operation)
    ```

### 5️⃣ Strategy Pattern 
- Why? Encapsulates different arithmetic operations as interchangeable strategies.  
- Where? `operation.py`  
- Implementation: 
  - Code: [`calculator/operation.py`]
  - Example:  
    ```python
    def addition(value1: Decimal, value2: Decimal) -> Decimal:
        return value1 + value2
    ```

---

## 🌍 Environment Variables Usage 

We use environment variables to configure logging levels, file paths, and application behavior dynamically.  

- Where? Environment variables are loaded via `dotenv` in [`calculator/commands/__init__.py`] 
- Implementation:  
  ```python
  from dotenv import load_dotenv, dotenv_values
  load_dotenv()
  env_vars = dotenv_values(".env")  
  logging.info("Loaded environment variables.")
  logging.debug("Environment Variables: %s", env_vars)
