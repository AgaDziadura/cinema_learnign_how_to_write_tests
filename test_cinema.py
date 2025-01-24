import unittest
from cinema import Seat, CinemaHall


class BookingSystemTests(unittest.TestCase):

    def setUp(self):
        # Initial setup for the tests
        self.hall = CinemaHall(rows=5, seats_per_row=10)

    def test_validate_valid_seat(self):
        # Test to validate if an allowed seat can be added
        seat = Seat(number=11, row=3)
        try:
            self.hall.add_seat(seat)
        except ValueError:
            self.fail("ValueError exception was raised.")

    def test_validate_invalid_seat(self):
        # Test to validate an invalid seat number or row
        with self.assertRaises(ValueError):
            seat = Seat(number=12, row=3)  # Seat out of acceptable range
            self.hall.add_seat(seat)

    def test_validate_correct_age(self):
        # Test to validate if age is eligible for a discount
        self.hall.reserve_seat(number=5, row=3, age=80, day_of_week=1)
        seat = self.hall.search_seat(number=5, row=3)
        self.assertLess(seat.get_price(), 10)  # Check if the price is less than 10

    def test_validate_incorrect_age(self):
        # No exception is expected but the discount should not be applied
        self.hall.reserve_seat(number=5, row=5, age=40, day_of_week=5)
        seat = self.hall.search_seat(5, 5)
        self.assertEqual(seat.get_price(), 10)  # Price without discount

    def test_validate_correct_day(self):
        # Test to validate if the day is Wednesday to apply discount
        self.hall.reserve_seat(number=5, row=3, age=45, day_of_week=2)
        seat = self.hall.search_seat(number=5, row=3)
        self.assertLess(seat.get_price(), 10)  # Check if the price is less than 10

    def test_validate_incorrect_day(self):
        # No exception is expected but the discount should not be applied
        self.hall.reserve_seat(number=5, row=3, age=25, day_of_week=3)
        seat = self.hall.search_seat(5, 3)
        self.assertEqual(seat.get_price(), 10)  # Price without discount

    def test_reserve_duplicate_seat(self):
        # Test to handle the exception of reserving an already reserved seat
        self.hall.reserve_seat(number=5, row=3, age=25)
        with self.assertRaises(ValueError) as context:
            self.hall.reserve_seat(number=5, row=3, age=25)
        self.assertEqual(str(context.exception), "The seat is already reserved.")

    def test_cancel_nonexistent_reservation(self):
        # Test to handle the exception of canceling a nonexistent reservation
        with self.assertRaises(ValueError) as context:
            self.hall.cancel_reservation(number=7, row=3)
        self.assertIn("The seat is not reserved.", str(context.exception))


if __name__ == "__main__":
    unittest.main()
