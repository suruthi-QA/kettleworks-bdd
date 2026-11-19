Feature: Shop listing - search, filter, sort and pagination
  As a shopper
  I want to find products quickly
  So that I can buy what I need

  Background:
    Given I am on the shop page

  @TC-01 @smoke
  Scenario: Home page shows the first page of products
    Then I should see 6 products
    And the pager should show "Page 1 of 3"

  @TC-02 @smoke
  Scenario: Search with matching case
    When I search for "Kadai"
    Then I should see "Cast Iron Kadai, 24cm" in the results

  @TC-03 @BUG-08
  Scenario: Search ignores upper and lower case
    When I search for "kadai"
    Then I should see "Cast Iron Kadai, 24cm" in the results

  @TC-04 @BUG-09
  Scenario: Search with no match shows an empty state
    When I search for "xyz123"
    Then no products should be listed
    And the loading spinner should not be visible

  @TC-05
  Scenario Outline: Filter by category
    When I select the category "<category>"
    Then every listed product should belong to "<category>"

    Examples:
      | category |
      | Cookware |
      | Bakeware |
      | Tools    |
      | Storage  |

  @TC-06
  Scenario: Sort by price, low to high
    When I sort by "Price, low to high"
    Then the prices should be in ascending order

  @TC-07
  Scenario: Sort by price, high to low
    When I sort by "Price, high to low"
    Then the prices should be in descending order

  @TC-08 @BUG-10
  Scenario: Sorting keeps the category filter
    When I select the category "Bakeware"
    And I sort by "Price, low to high"
    Then the category filter should still be "Bakeware"
    And every listed product should belong to "Bakeware"

  @TC-09 @BUG-11
  Scenario: Every product appears exactly once across pages
    When I go through all pages
    Then each product should appear only once
    And the number of listed products should match the API

  @TC-10
  Scenario: Previous button is disabled on the first page
    Then the "Previous" button should be disabled
