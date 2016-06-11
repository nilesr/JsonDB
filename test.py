import BTEdb
db = BTEdb.Database("x.json", 4)
def reset(db):
    db.Create("main table")
    db.Insert("main table", UID = 0, username = "root",favColor = 0xffffff)
    db.Insert("main table", UID = 1, username = "Ethan",favColor = 0xffffff)
    db.Insert("main table", UID = 2, username = "Niles",favColor = 0xffffff)
reset(db)
assert(len(db.Dump("main table")) == 3)
assert(db.Select("main table", UID = 1)[0]["username"] == "Ethan")
assert(db.Select("main table", username = "Niles", favColor = 0xffffff)[0]["UID"] == 2)
assert(len(db.Select("main table", lambda x: x["UID"] > 0)) == 2)
db.Insert("main table", ["UID", 3], ["username", "nobody"], favColor = 0)
assert(db.Select("main table", UID = 3)[0] == {"favColor": 0, "username": "nobody", "UID": 3})
assert(len(db.Select("main table", lambda x: x["favColor"] != 0, lambda x: x["UID"] > 0)) == 2)
assert(len(db.Select("main table", lambda x: x["favColor"] != 0, lambda x: x["UID"] > 0, username = "Niles")) == 1)
assert(db.Delete("main table", lambda x: x["UID"] > 0)[0]["UID"] > 0)
assert(len(db.Dump("main table")) == 1)
assert(db.Select("main table", username = "root")[0]["favColor"] == 0xffffff)
reset(db)
db.Delete("main table", UID = 0)
assert(len(db.Dump("main table")) == 2)
reset(db)
db.Delete("main table", lambda x: x["UID"] > 1, UID = 0)
assert(len(db.Dump("main table")) == 3)
assert(len(db.Delete("main table", lambda x: x["UID"] > 1, username = "Niles")) == 1)
assert(len(db.Dump("main table")) == 2)
reset(db)
db.Insert("main table", a = "b", c = "d")
db.Delete("main table", UID = 0)
assert(db.Select("main table", a = "b")[0]["c"] == "d")
assert(len(db.Dump("main table")) == 3)
db.Update("main table", db.Select("main table", a = "b"), e = "f")
assert(db.Select("main table", a = "b")[0]["e"] == "f")
db.Update("main table", db.Select("main table", a = "b"), ["g", "h"])
assert(db.Select("main table", a = "b")[0]["g"] == "h")
reset(db)
db.Update("main table", db.Select("main table", UID = 0), favColor = 0xeeeeee)
db.Update("main table", db.Dump("main table"), is_root = False)
db.Update('main table', db.Select("main table", lambda x: x["UID"] == 0 or x["username"] == "root"), is_root = True)
assert(len(db.Select("main table", is_root = True)) == 1)
assert(db.Select("main table", is_root = True)[0]["favColor"] == 0xeeeeee)
db.Insert("main table", *[["UID", 3], ["is_root", False]], username = "Bryan")
assert(not db.Select("main table", lambda x: x["username"] == "Bryan", UID = 3)[0]["is_root"])
reset(db)
db.BeginTransaction()
db.Delete("main table", lambda x: True)
assert(len(db.Dump("main table")) == 0)
db.Create("table 2")
db.Insert("table 2", year = 1998)
assert(len(db.Dump("table 2")) == 1)
db.RevertTransaction()
assert(len(db.Dump("main table")) == 3)
assert(len(db.Dump("table 2")) == 1)
s = False
db.BeginTransaction(False)
try:
    db.RevertTransaction()
except BTEdb.TransactionNotRevertableException:
    s = True
assert(s)
db.Drop("table 2")
s = False
try:
    db.Drop("table 2")
except BTEdb.TableDoesNotExistException:
    s = True
assert(s)
reset(db)
assert(len(db.Dump("main table")) == 3)
db.Truncate("main table")
assert(len(db.Dump("main table")) == 0)
s = False
try:
    db.Truncate("table 2")
except BTEdb.TableDoesNotExistException:
    s = True
assert(s)
assert(db.ListTables() == ["main table"])
assert(db.TableExists("main table"))
assert(not db.TableExists("table 2"))
reset(db)
db.Save("name")
db.Save("name 2", "main table")
db.Truncate("main table")
db.Create("table 2")
db.Insert("table 2", UID = 0, username = "root")
db.Revert("name")
assert(len(db.Dump("main table")) == 3)
assert(len(db.Dump("table 2")) == 1)
db.Truncate("main table")
db.Insert("table 2", UID = 1, username = "Niles")
db.Revert("name 2", "main table")
assert(len(db.Dump("main table")) == 3)
assert(len(db.Dump("table 2")) == 2)
db.RemoveSave("name 2")
assert(db.ListSaves() == ["name"])
assert(db.SaveExists("name"))
assert(not db.SaveExists("name 2"))
x = db.GetSave("name")
assert("main table" in x)
db.Truncate("main table")
db.PutSave(x, "name 2")
db.Revert("name 2")
assert(len(db.Dump("main table")) == 3)
x = db.GetSave()
assert("name" in x)
# TODO: Test triggers
