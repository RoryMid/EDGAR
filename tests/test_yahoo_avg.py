# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 16:21:12 2021

"""

import pytest

import Edgar.joins as j
#j.yahoo_avg()


def test_yahoo_columns():
    actual_result = len(j.yahoo_avg().columns)
    expected_result = 7
    assert actual_result == expected_result


def test_yahoo_rows():
    expected_result = 5134
    actual_result = len(j.yahoo_avg().index)
    assert actual_result == expected_result


