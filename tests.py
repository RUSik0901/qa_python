import pytest
from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_genre()) == 2

    @pytest.fixture
    def collector(self):
        return BooksCollector()

    def test_add_new_book_success(self, collector):
        collector.add_new_book('Гордость и предубеждение и зомби')
        assert len(collector.get_books_genre()) == 1  # Проверяем, что добавилась одна книга
        assert 'Гордость и предубеждение и зомби' in collector.get_books_genre()  # Проверяем, что книга добавлена

    def test_add_new_book_invalid_name_empty(self, collector):
        collector.add_new_book("")  # Пустое имя книги
        assert len(collector.get_books_genre()) == 0  # Книга не должна добавляться

    def test_add_new_book_invalid_name_too_long(self, collector):
        long_book_name = "A" * 41  # Имя книги превышает 40 символов
        collector.add_new_book(long_book_name)
        assert len(collector.get_books_genre()) == 0  # Книга не должна добавляться

    def test_add_duplicate_book(self, collector):
        book_name = "1984"
        collector.add_new_book(book_name)  # Добавляем книгу первый раз
        assert len(collector.get_books_genre()) == 1  # Проверяем, что книга добавлена
        collector.add_new_book(book_name)  # Пытаемся добавить книгу второй раз
        assert len(collector.get_books_genre()) == 1  # Проверяем, что книга добавлена только один раз

    def test_set_book_genre_success(self, collector):
        book_name = "Мастер и Маргарита"
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, "Фантастика")
        assert collector.get_book_genre(book_name) == "Фантастика"  # Проверяем, что жанр установлен правильно

    def test_set_book_genre_invalid(self, collector):
        collector.set_book_genre("Несуществующая книга", "Фантастика")
        assert collector.get_book_genre("Несуществующая книга") is None  # Жанр не должен устанавливаться

    def test_get_book_genre(self, collector):
        book_name = "Война и мир"
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, "Фантастика")
        assert collector.get_book_genre(book_name) == "Фантастика"  # Проверяем, что жанр возвращается правильно

    def test_get_books_with_specific_genre(self, collector):
        collector.add_new_book("Война и мир")
        collector.set_book_genre("Война и мир", "Фантастика")
        collector.add_new_book("Оно")
        collector.set_book_genre("Оно", "Ужасы")
        fantasy_books = collector.get_books_with_specific_genre("Фантастика")
        assert fantasy_books == ["Война и мир"]  # Проверяем, что возвращается правильный список книг

    def test_get_books_for_children(self, collector):
        collector.add_new_book("Детская книга")
        collector.set_book_genre("Детская книга", "Мультфильмы")
        collector.add_new_book("Страшная книга")
        collector.set_book_genre("Страшная книга", "Ужасы")
        children_books = collector.get_books_for_children()
        assert "Детская книга" in children_books  # Проверяем, что книга для детей в списке
        assert "Страшная книга" not in children_books  # Проверяем, что книга с возрастным рейтингом не в списке

    def test_add_book_in_favorites(self, collector):
        book_name = "1984"
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        assert book_name in collector.get_list_of_favorites_books()  # Проверяем, что книга в избранном

    def test_delete_book_from_favorites(self, collector):
        book_name = "1984"
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.delete_book_from_favorites(book_name)
        assert book_name not in collector.get_list_of_favorites_books()  # Проверяем, что книга удалена из избранного

    def test_get_list_of_favorites_books(self, collector):
        book1 = "1984"
        book2 = "Мастер и Маргарита"
        collector.add_new_book(book1)
        collector.add_new_book(book2)
        collector.add_book_in_favorites(book1)
        collector.add_book_in_favorites(book2)
        favorites = collector.get_list_of_favorites_books()
        assert set(favorites) == {book1, book2}  # Проверяем, что оба книги в избранном

    def test_get_books_genre(self, collector):
        collector.add_new_book("Война и мир")
        collector.set_book_genre("Война и мир", "Фантастика")
        collector.add_new_book("1984")
        collector.set_book_genre("1984", "Детективы")
        expected_genre_dict = {
            "Война и мир": "Фантастика",
            "1984": "Детективы"
        }
        assert collector.get_books_genre() == expected_genre_dict  # Проверяем, что возвращается правильный словарь