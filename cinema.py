"""
I assume that the following application is intended for cinema workers and not for online purchases since not everyone
should be able to freely add seats or apply for discounts by entering their age without showing an accreditation document.
Additionally, to avoid errors, it is assumed that both the reservation and the operation of showing seats work for the
current date/day.
"""

from datetime import datetime


class Seat:
    def __init__(self, number, row):
        # First we make sure that the number entered for both the seat number and row are integers greater than 0.
        if not isinstance(number, int) or number <= 0:
            raise ValueError("The seat number must be a positive integer.")
        if not isinstance(row, int) or row <= 0:
            raise ValueError("The seat row must be a positive integer.")
        self.__number = number
        self.__row = row
        self.__reserved = False
        self.__price = 0

    def get_number(self):
        return self.__number  # returns the value of the number variable

    def get_row(self):
        return self.__row  # returns the value of the row variable

    def is_reserved(self):
        return self.__reserved  # returns a boolean value depending on whether the seat is reserved or not

    def set_reserved(self, reserved):
        self.__reserved = reserved  # changes the reserved seat status to True/False

    def get_price(self):
        return self.__price  # returns the value of the price variable

    def set_price(self, price):
        self.__price = price  # assigns a value to the price variable


class CinemaHall:
    def __init__(self, rows, seats_per_row):
        # First we make sure that the number entered for both the number of seats per row and the total number of rows
        # are integers greater than 0.
        if not isinstance(seats_per_row, int) or seats_per_row <= 0:
            raise ValueError("The number of seats in each row must be a positive integer.")
        if not isinstance(rows, int) or rows <= 0:
            raise ValueError("The total number of rows must be a positive integer.")
        # We build a list that will contain all the seats in all the rows in the movie theater
        self.__seats = []
        for row in range(1, rows + 1):
            for number in range(1, seats_per_row + 1):
                self.__seats.append(Seat(number, row))

    def get_rows(self):
        return len(set([seat.get_row() for seat in self.__seats]))

    def get_seats_per_row(self):
        return len(set([seat.get_number() for seat in self.__seats]))

    def reserve_seat(self, number, row, age, day_of_week=datetime.today().weekday(),
                     base_price=10):  # default base price: €10
        # For the discount to be applied automatically if the day is Wednesday, we take the current day using the
        # datetime library
        seat = self.search_seat(number, row)
        if seat:
            if not seat.is_reserved():
                price = base_price
                if day_of_week == 2:  # Wednesday
                    price *= 0.8
                if age > 65:
                    price *= 0.7
                seat.set_price(price)
                seat.set_reserved(True)
                return f"Seat {number} in row {row} has been reserved. Price: {price:.2f}€"
            else:
                raise ValueError("The seat is already reserved.")
        else:
            raise ValueError("The seat does not exist.")


    def cancel_reservation(self, number, row):
        seat = self.search_seat(number, row)
        if seat:
            if seat.is_reserved():
                seat.set_reserved(False)
                seat.set_price(0)
                return f"Reservation for seat {number} in row {row} has been canceled."
            else:
                raise ValueError("The seat is not reserved.")
        else:
            raise ValueError("The seat does not exist.")


    def add_seat(self, seat):
        # Verify if a seat like this already exists
        for a in self.__seats:
            if a.get_number() == seat.get_number() and a.get_row() == seat.get_row():
                raise ValueError("The seat is already registered in the hall.")

        # Get number of seats per row. It is decided to leave the possibility of adding seats only in existing rows
        # and as a continuation of a row.
        if self.__seats:
            last_row = self.__seats[-1].get_row()
            if seat.get_row() > last_row:
                raise ValueError(
                    f"The row number is greater than the total number of rows in the hall. Creating new rows is not allowed."
                    f"Seats can be added in rows from {self.__seats[0].get_row()} to {last_row}.")
            last_number = self.__seats[-1].get_number()
            if seat.get_number() != last_number + 1:
                raise ValueError(
                    f"The seat number is not the next in the row. It is only allowed to add seats in order. "
                    f"The number of the next available seat is: {last_number + 1}.")

        # Insert the seat in the correct position in the seat list
        position = 0
        for a in self.__seats:
            if seat.get_row() < a.get_row() or (
                    seat.get_row() == a.get_row() and seat.get_number() < a.get_number()):
                break
            position += 1

        self.__seats.insert(position, seat)
        return f"Seat {seat.get_number()} in row {seat.get_row()} has been added."

    def show_seats(self, day_of_week=datetime.today().weekday(), base_price=10):
        # We create a list of all the seats to show their availability and price
        all_seats = []
        if day_of_week == 2:  # Wednesday
            base_price *= 0.8
        for seat in self.__seats:
            status = "Reserved" if seat.is_reserved() else "Available"
            if seat.is_reserved():
                price = seat.get_price()
            else:
                price = base_price
            all_seats.append(f"Seat {seat.get_number()}, row {seat.get_row()}: {status}, Price: {price}€")
        return "\n".join(all_seats)

    def search_seat(self, number, row):
        for seat in self.__seats:
            if seat.get_number() == number and seat.get_row() == row:
                return seat
        return None


# Usage examples
if __name__ == "__main__":
    # First we create a movie theater with rows and seats per row according to our criteria
    hall = CinemaHall(rows=7, seats_per_row=10)

    # See all available seats in the created room with their corresponding price depending on the day
    print(hall.show_seats())

    '''Reserve the seat chosen by the worker. For this we ask you to enter the seat number, 
    the row number and the age of the client, which must be a positive integer and less than 110.'''
    if __name__ == "__main__":
        hall = CinemaHall(5, 5)  # Create an instance of CinemaHall

        while True:
            client_number = int(input("Enter the seat number: "))
            client_row = int(input("Enter the seat row: "))
            client_age = int(input("Enter the age: "))

            # Input validation
            if not 1 <= client_number <= hall.get_seats_per_row():
                raise ValueError("Invalid seat number.")
            if not 1 <= client_row <= hall.get_rows():
                raise ValueError("Invalid seat row.")
            if not 0 <= client_age <= 120:  # Reasonable age range
                raise ValueError("Invalid age.")

            print(hall.reserve_seat(number=client_number, row=client_row, age=client_age))

            # Option to reserve another seat
            again= input("Do you want to reserve another seat? (y/n): ")
            if again.lower() != 'y':
                break

    # Reserve a specific seat
    print(hall.reserve_seat(number=5, row=5, age=70))

    # Show seats after booking
    print(hall.show_seats())

    # Add a specific seat
    print(hall.add_seat(Seat(number=6, row=3)))

    # Cancel reservation of a specific seat
    print(hall.cancel_reservation(number=5, row=5))
