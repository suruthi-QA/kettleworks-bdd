Feature: Admin shop tools

  @TC-52 @BUG-19 @security
  Scenario: Guest cannot open the admin page
    Given I am not signed in
    When I open "/admin"
    Then I should not see the text "Shop tools"

  @TC-53 @LBUG-02 @security
  Scenario: Customer cannot open the admin page
    Given I sign in as the customer
    When I open "/admin"
    Then I should not see the text "Shop tools"

  @TC-55 @smoke
  Scenario: Admin sees every product and the right stock value
    Given I sign in as the admin
    When I open "/admin"
    Then the admin table should list every product
    And the stock value should equal price multiplied by stock for all products

  @TC-56 @ABUG-02
  Scenario: Restock increases the stock of an item
    Given I sign in as the admin
    When I open "/admin"
    And I click Restock for "Carbon Steel Tawa, 28cm"
    Then the stock of "Carbon Steel Tawa, 28cm" should be more than 0
