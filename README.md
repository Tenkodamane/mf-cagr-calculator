# Mutual Fund SIP CAGR Analysis

Tiny Dashboard for mutual fund SIP CAGR and analysis

<img alt="Mutual Fund portfolio" src="https://github.com/Tenkodamane/mf-cagr-calculator/blob/main/out/MF_Performance.png" width="300">

## Features

- Calculate CAGR for given portfolio
- Generate summary of your portfolio
- Graphical presentation of CAGR's


### Download

```
git clone https://github.com/BaseMax/MiniCalculatorInterpreter
cd MiniCalculatorInterpreter
sudo pip3 install ply
python calculator.py
```


### Using

```
python main.py --inputXl input.xlsx --configFile config.json --outputFile output.xlsx
```

### Input xl file required fields 

```
1. Investment Date
2. Quantity
3. Price when NAV allocated
4. Profit
5. Age (Number of days)
```
Example: input.xlsx

### config file
Script expects below key to be mapped with column heading in case the input.xlsx having different naming
For below key's update the values according to input.xlsx column heading
```
1. invested_date
2. price
3. qty
4. age
5. profit
```
Refer the config.json

---
**NOTE**

- The above input.xlsx is taken from Zerodha console(https://console.zerodha.com/portfolio/holdings)
- This step may be different for different brokerage account
- Tested only with data taken from Zerodha console
---
