import io_module
import stack_module
import file_module
from prettytable import PrettyTable


def display_menu(stack):
    while True:
        print("/------------------------------------------------------------------------------")
        print("| Меню:                                                                        |")
        print("| 1. Создать нового клиента                                                    |")
        print("| 2. Вывести данные в формате 'поле: значение'                                 |")
        print("| 3. Вывести данные в табличном формате                                        |")
        print("| 4. Сохранить данные в файл                                                   |")
        print("| 5. Загрузить данные из файла                                                 |")
        print("| 6. Удалить файл базы данных                                                  |")
        print("| 7. Отсортировать данные                                                      |")
        print("| 8. Поиск клиента                                                             |")
        print("| 9. Удалить клиента по индексу                                                |")
        print("| 10. Изменить данные клиента                                                  |")
        print("| 0. Выход                                                                     |")
        print("-------------------------------------------------------------------------------/")
        choice = input("Выберите действие: ")
        try:
            choice = int(choice)
        except ValueError:
            print("Ошибка: введите числовое значение")
            continue

        if choice == 0:
            print("Выход")
            break
        elif choice == 1:
            try:
                new_client = io_module.read_data()
                stack_module.push(stack, new_client)
            except Exception as e:
                print(f"Ошибка: {e}")
        elif choice == 2:
            if not stack_module.is_empty(stack):
                try:
                    index = int(input("Введите номер клиента в стеке: "))
                    client = stack_module.get_client_index(stack, index)
                    if client:
                        io_module.print_data(client)
                    else:
                        print("Клиент с указанным номером не найден")
                except ValueError:
                    print("Ошибка: введите числовое значение")
            else:
                print("Стек пуст")
        elif choice == 3:
            if not stack_module.is_empty(stack):
                show_table(stack)
            else:
                print("Стек пуст")
        elif choice == 4:
            try:
                file_module.save_db(stack, "database.txt")
            except Exception as e:
                print(f"Ошибка при сохранении данных: {e}")
        elif choice == 5:
            try:
                file_module.load_db(stack, "database.txt")
            except Exception as e:
                print(f"Ошибка при загрузке данных: {e}")
        elif choice == 6:
            try:
                file_module.remove_db("database.txt")
            except Exception as e:
                print(f"Ошибка при удалении файла: {e}")
        elif choice == 7:
            sort_fields = ["login", "password", "balance", "email", "address"]
            print("Поля для сортировки:")
            for i, field in enumerate(sort_fields, start=1):
                print(f"{i}. {field.capitalize()}")
            try:
                sort_choice = int(input("Введите номер поля для сортировки: "))
                if 1 <= sort_choice <= len(sort_fields):
                    key = sort_fields[sort_choice - 1]
                else:
                    raise ValueError
            except ValueError:
                print("Ошибка: некорректный ввод поля для сортировки")
                continue

            try:
                direction_choice = int(input("Введите направление сортировки (1 для возрастания, 2 для убывания): "))
                if direction_choice == 1:
                    reverse = False
                elif direction_choice == 2:
                    reverse = True
                else:
                    raise ValueError
            except ValueError:
                print("Ошибка: некорректный ввод направления сортировки")
                continue

            try:
                stack_module.sort_data(stack, key, reverse)
            except Exception as e:
                print(f"Ошибка при сортировке данных: {e}")
        elif choice == 8:
            key = input("Введите поле для поиска (login, password, balance, email, address): ")
            value = input("Введите значение для поиска: ")
            try:
                results = stack_module.search_client(stack, key, value)
                if results:
                    for index, client in results:
                        print(f"Индекс: {index}")
                        io_module.print_data(client)
                else:
                    print("Клиенты с указанными данными не найдены")
            except KeyError:
                print("Ошибка: некорректное поле для поиска")
            except Exception as e:
                print(f"Ошибка при поиске клиента: {e}")
        elif choice == 9:
            try:
                index = int(input("Введите индекс клиента для удаления: "))
                if stack_module.delete_client(stack, index):
                    print("Клиент успешно удален")
                else:
                    print("Ошибка при удалении клиента")
            except ValueError:
                print("Ошибка: введите числовое значение")
            except Exception as e:
                print(f"Ошибка при удалении клиента: {e}")
        elif choice == 10:
            try:
                index = int(input("Введите индекс клиента для изменения: "))
                key = input("Введите поле для изменения (login, password, balance, email, address): ")
                new_value = input(f"Введите новое значение для поля {key}: ")
                if stack_module.update_client(stack, index, key, new_value):
                    print("Данные клиента успешно обновлены")
                else:
                    print("Ошибка при обновлении данных клиента")
            except ValueError:
                print("Ошибка: введите числовое значение")
            except KeyError:
                print("Ошибка: некорректное поле для изменения")
            except Exception as e:
                print(f"Ошибка при обновлении данных клиента: {e}")
        else:
            print("Некорректный ввод")


def show_table(stack):
    table = PrettyTable()
    table.field_names = ["Индекс", "Login", "Пароль", "Баланс", "Email", "Адрес"]

    current = stack.top
    index = 0
    while current:
        client = current.data
        table.add_row(
            [index, client['login'], client['password'], client['balance'], client['email'], client['address']])
        current = current.next
        index += 1

    print(table)
