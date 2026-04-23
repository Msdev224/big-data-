INSERT INTO category (id, code, intitule) VALUES
(1, 'CAT-FIC', 'Fiction'),
(2, 'CAT-SCI', 'Science'),
(3, 'CAT-BIZ', 'Business');

INSERT INTO books (id, category_id, code, intitule, isbn_10, isbn_13, prix_catalogue) VALUES
(1, 1, 'BK-001', 'Le Roman Moderne', '1234567890', '9781234567890', 18.50),
(2, 2, 'BK-002', 'Introduction au Big Data', '1234567891', '9781234567891', 32.00),
(3, 3, 'BK-003', 'Management Agile', '1234567892', '9781234567892', 25.00),
(4, 2, 'BK-004', 'Cloud Analytics', '1234567893', '9781234567893', 29.90),
(5, 1, 'BK-005', 'Nouvelles Africaines', '1234567894', '9781234567894', 15.00);

INSERT INTO customers (id, code, first_name, last_name, email, city, country) VALUES
(1, 'CUST-001', 'Aline', 'Mbida', 'aline@example.com', 'Douala', 'Cameroun'),
(2, 'CUST-002', 'Jean', 'Talla', 'jean@example.com', 'Yaounde', 'Cameroun'),
(3, 'CUST-003', 'Mireille', 'Nana', 'mireille@example.com', 'Bafoussam', 'Cameroun'),
(4, 'CUST-004', 'David', 'Kenfack', 'david@example.com', 'Paris', 'France');

INSERT INTO factures (id, customer_id, code, qte_totale, total_amount, total_paid, date_edit) VALUES
(1, 1, 'FAC-2025-001', 3, 82.50, 82.50, '20250312'),
(2, 2, 'FAC-2025-002', 2, 61.90, 61.90, '20250315'),
(3, 3, 'FAC-2025-003', 4, 90.00, 75.00, '20250320'),
(4, 4, 'FAC-2025-004', 1, 29.90, 29.90, '20250402');

INSERT INTO ventes (id, facture_id, book_id, pu, qte, date_edit) VALUES
(1, 1, 2, 32.00, 1, '20250312'),
(2, 1, 1, 18.50, 1, '20250312'),
(3, 1, 3, 32.00, 1, '20250312'),
(4, 2, 4, 29.90, 1, '20250315'),
(5, 2, 5, 32.00, 1, '20250315'),
(6, 3, 3, 25.00, 2, '20250320'),
(7, 3, 5, 15.00, 2, '20250320'),
(8, 4, 4, 29.90, 1, '20250402');
