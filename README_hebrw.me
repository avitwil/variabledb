

# מדריך שימוש – VariableDB

## תקציר

`VariableDB` הוא מחלקה לניהול משתנים בזיכרון עם אפשרות לשמירה וטעינה מקובץ `.db` באמצעות ספריית `dill`. המטרה היא לאפשר שליטה נוחה על משתנים, כולל שמירה לקובץ, טעינה, מחיקה ועדכון – בצורה שקופה וידידותית.

---

## דרישות מקדימות

* Python 3.7+
* חבילת `dill` מותקנת:

```bash
pip install dill
```

---

## יצירת מופע של `VariableDB`

```python
from variabledb import VariableDB

db = VariableDB("my_data", scope=globals())
```

* `filename`: שם הקובץ לשמירה (ללא צורך להוסיף `.db`).
* `scope`: מילון הסקופ, לרוב `globals()`, שאליו המשתנים יטענו.

---

## מבנה כללי

```python
db = VariableDB("my_file", scope=globals())
```

* `data`: מילון פנימי המאחסן את המשתנים.
* `scope`: הסביבה שאליה יוזרקו המשתנים בעת טעינה.
* `filename`: שם קובץ שבו יישמר המידע (מאובטח מולידציה שיסתיים ב־`.db`).

---

## פונקציונליות מלאה

### 1. `add(variable, name=None)`

שומר משתנה בודד למסד.

```python
x = 42
db.add(x)  # יזהה את השם "x" לבד

db.add(x, name="my_number")  # בשם מותאם
```

> אם לא נשלח שם, `VariableDB` תנסה למצוא אותו לפי הסקופ.

---

### 2. `add_multiple(**variables)`

שומר כמה משתנים בבת אחת:

```python
db.add_multiple(a=1, b=2, c=[3, 4])
```

> במקרה של כשל, תיזרק `RuntimeError` עם מידע על המשתנים שלא נשמרו.

---

### 3. `__setitem__(key, value)` ו־`__getitem__`

גישה למשתנים כמו למילון:

```python
db["x"] = 99
print(db["x"])  # 99
```

---

### 4. `save()`

שומר את כל המשתנים לקובץ `.db` באמצעות `dill`.

```python
db.save()
```

---

### 5. `load()`

טוען נתונים מקובץ קיים, ומעדכן את הסקופ שנשלח.

```python
db.load()
print(x)  # אם x נשמר קודם, הוא יופיע עכשיו
```

---

### 6. שימוש עם `with` (context manager)

```python
with VariableDB("my_file", scope=globals()) as db:
    db["counter"] = 5
# נשמר אוטומטית ביציאה מהבלוק
```

---

### 7. `delete(name: str)`

מוחק משתנה לפי מפתח:

```python
db.delete("x")
```

> ייזרקו חריגות אם השם לא קיים או לא מחרוזת.

---

### 8. `clear()`

מוחק את כל המשתנים במסד:

```python
db.clear()
```

---

### 9. `update(variables: dict, overwrite=True)`

מעדכן את המסד עם מילון משתנים:

```python
db.update({"x": 1, "y": 2})

db.update({"x": 3}, overwrite=False)  # לא ישנה את x
```

---

### 10. `get(key, default=None)`

בדומה ל־`dict.get`:

```python
value = db.get("x", default=0)
```

---

### 11. `__delitem__(key)`

מוחק משתנה:

```python
del db["x"]
```

---

### 12. `__contains__(key)`

בודק אם קיים משתנה בשם מסוים:

```python
if "x" in db:
    print("x is in the database")
```

---

### 13. `__len__()`

מספר המשתנים:

```python
print(len(db))
```

---

### 14. `__iter__()`

מאפשר לולאה על משתנים:

```python
for name, value in db:
    print(name, value)
```

---

### 15. `__bool__()`

בודק אם יש נתונים:

```python
if db:
    print("Database is not empty")
```

---

### 16. `__str__()` ו־`__repr__()`

הצגה ידידותית של התוכן:

```python
print(db)
```

---

## דוגמת שימוש מלאה

```python
from variabledb import VariableDB

x = 100
name = "Alice"

with VariableDB("session", scope=globals()) as db:
    db.add(x)
    db.add(name)
    db["score"] = 9000
    db.update({"level": 5, "items": ["sword", "shield"]})

# טוען בהפעלה מחדש
new_db = VariableDB("session", scope=globals())
new_db.load()

print(x)        # 100
print(score)    # 9000
```

---

## הערות טכניות

* הקובץ ייווצר אוטומטית אם אינו קיים.
* אם הספרייה לא קיימת – תיווצר.
* אם הקובץ קיים – הנתונים ייטענו ממנו.
* שמות משתנים מתגלים אוטומטית רק אם קיימים ב־scope.

---

## קובץ לוג

נוצר אוטומטית בקובץ `variabledb_log.log` עם פרטי שגיאות ותקלות.

---

## רישיון

המודול לשימוש חופשי. ניתן להרחיב, לשפר ולשתף בהתאם לרישוי שאתה תבחר לצרף.


