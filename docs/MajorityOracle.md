* [MajorityOracle](#majorityoracle)
  * [Accessors](#majorityoracle-accessors)
  * [Functions](#majorityoracle-functions)
    * [getStatusAndOutcome()](#getstatusandoutcome)
    * [getOutcome()](#getoutcome)
    * [isOutcomeSet()](#isoutcomeset)

# MajorityOracle

### Majority oracle contract - Allows to resolve an event based on multiple oracles with majority vote

- **Author**: Stefan George - <stefan@gnosis.pm>
- **Constructor**: MajorityOracle(*address[]* `_oracles`)
- This contract does **not** have a fallback function.

## MajorityOracle Accessors

* *address* oracles(*uint256*) `5b69a7d8`

## MajorityOracle Functions

### getStatusAndOutcome()

- **State mutability**: `nonpayable`
- **Signature hash**: `6bcc035a`

Allows to registers oracles for a majority vote

#### Outputs

| type     | name         |
| -------- | ------------ |
| *bool*   | `outcomeSet` |
| *int256* | `outcome`    |

### getOutcome()

- **State mutability**: `view`
- **Signature hash**: `7e7e4b47`

Returns winning outcome

#### Outputs

| type     | description |
| -------- | ----------- |
| *int256* | Outcome     |

### isOutcomeSet()

- **State mutability**: `view`
- **Signature hash**: `ccdf68f3`

Returns if winning outcome is set

#### Outputs

| type   | description     |
| ------ | --------------- |
| *bool* | Is outcome set? |
