# Stock Market Range Analysis Using Segment Tree 

## About the Project

This project is about analyzing stock prices using a Segment Tree data structure.

When working with stock market data, we may need to find the total, minimum, or maximum stock price over a particular range of days. Doing these operations repeatedly using a normal array can take more time, especially when the data is large.

To solve this problem, I implemented a Segment Tree in Python. It helps perform range queries and update stock prices more efficiently.

The project also includes an interactive menu that allows users to explore stock price data and perform different operations.

## What Can You Do With This Project?

Here are some of the operations supported by the program:

* Find the total stock price over a selected range of days
* Find the minimum stock price in a range
* Find the maximum stock price in a range
* Calculate the average stock price over a range
* Analyze stock price volatility
* Update the stock price of a particular day
* Insert a new stock price
* Delete an existing stock price

## Why Did I Use a Segment Tree?

A Segment Tree is useful when we need to perform multiple range queries and updates on an array.

Instead of checking every stock price whenever a query is made, the Segment Tree stores information about different ranges. This helps answer queries more efficiently.

In this project, each node stores the sum, minimum, and maximum stock price for its corresponding range.

## Technologies Used

* Python
* Data Structures and Algorithms
* Segment Tree

## Time Complexity

| Operation                 | Time Complexity |
| ------------------------- | --------------- |
| Building the Segment Tree | O(n)            |
| Range Sum Query           | O(log n)        |
| Range Minimum Query       | O(log n)        |
| Range Maximum Query       | O(log n)        |
| Updating a Stock Price    | O(log n)        |
| Insertion and Deletion    | O(n)            |
| Space Complexity          | O(n)            |

## How to Run the Project

Make sure Python 3 is installed on your system.

1. Clone or download this repository.
2. Open the project folder in your terminal.
3. Run the Python file:

```bash
python stock_market_analysis.py
```

Replace the filename with the actual name of your Python file if it is different.

## What I Learned

While working on this project, I got a better understanding of how Segment Trees work and how they can be used to solve real-world problems.

I also learned how to perform range queries, update values efficiently, and analyze the time complexity of different operations.

This project helped me improve my understanding of Data Structures and Algorithms by applying them to a stock market analysis problem.

---

**Project:** Stock Market Range Analysis Using Segment Tree
**Language:** Python
**Data Structure:** Segment Tree
