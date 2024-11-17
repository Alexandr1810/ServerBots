import pickle
update_id = 12

# сохраняем
with open('data.sav', 'wb') as f:
  pickle.dump(update_id, f)

update_id = 0

# Получаем
with open('data.sav', 'rb') as f:
  update_id = pickle.load(f)
print(update_id)