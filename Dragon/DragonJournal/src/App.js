import React from 'react';
import { Button,
         Collapse,
         Navbar,
         NavbarToggler,
         NavbarBrand,
         Nav,
         NavItem,
         NavLink,
         UncontrolledDropdown,
         DropdownToggle,
         DropdownMenu,
         DropdownItem,
         Container,
         Row,
         Col,
         Input,
         Label } from 'reactstrap';


function GetLink(symbol)
{
  document.getElementById("Chart").src=`https://finviz.com/chart.ashx?t=${symbol}&ty=c&ta=1&p=d&s=l`
}

const ChartPanel = () =>
{
    return (
      <div>
        <Row>
          <Col sm="4" xs="4"></Col>
          <Col sm="4" xs="4">
            <Input
              id="SymbolName"
              placeholder="Enter Symbol Here"
              type="text"
              onChange={e => GetLink( e.target.value )}>
            </Input>
          </Col>
        </Row>
        <img id="Chart" src="https://finviz.com/chart.ashx?t=AAPL&ty=c&ta=1&p=d&s=l"></img>
        <Row>
          <Col sm="10" xs="10">
            <textarea id="JournalPad"></textarea>
          </Col>
          <Col sm="2" xs="2">
            <Button>Submit</Button>
          </Col>
        </Row>
      </div>
    )
};
  
class App extends React.Component
{
  constructor( props )
  {
    super( props );
    console.log( `Calculator::constructor():: props=${this.props.MAX_ACCOUNT_SIZE}`)

    this.state = {
      accountSize: 10000,
      riskPerTradePercent: 1,
      entryPrice: 15,
      stopLossPrice: 14.5,
      targetPrice: 15.5,
      numberOfShares: 0,
      profitPerShare: 0,
      returnOnAccountPercent: 2,
      stopLossPerShare: 0,
      totalCost: 0
    }

  }

  ComputeValues = () =>
  {
    var accountSize = parseFloat( document.getElementById( "AccountSize" ).value )
    var riskPerTradePercent = parseFloat( document.getElementById( "RiskPerTradePercent" ).value )
    var entryPrice = parseFloat( document.getElementById( "EntryPrice" ).value )
    var stopLossPrice = parseFloat( document.getElementById( "StopLossPrice" ).value )
    var returnOnAccountPercent = parseFloat( document.getElementById( "ReturnOnAccountSize" ).value )

    var riskValue = accountSize * ( riskPerTradePercent / 100 )

    console.log( `entryPrice=${entryPrice}` )

    var stopLossPerShare = entryPrice - stopLossPrice;

    var numShares = parseInt( riskValue / stopLossPerShare );
    console.log( `numShares=${numShares}` )

    console.log( `entryPrice=${entryPrice}, stopLossPerShare=${stopLossPerShare}`)
    var targetPrice = parseFloat( entryPrice ) + ( returnOnAccountPercent * parseFloat( stopLossPerShare ) );

    var totalCost = numShares * entryPrice;

    this.setState(
      {
        accountSize: accountSize,
        numberOfShares: numShares, 
        stopLossPerShare: stopLossPerShare, 
        targetPrice: targetPrice,
        profitPerShare: ( returnOnAccountPercent * stopLossPerShare ),
        totalCost: totalCost
      }
    )
  }

  // Inputs:
  ChangeAccountSize = value => 
  {
    // Validate:
    if ( value > 1000000 )
    {
      alert( "Account size must not exceed 1000000" )
    }
    this.ComputeValues() 
  }

  ChangeRiskPerTradePercent = value => this.setState( { riskPerTradePercent: value } )

  ChangeEntryPrice = value => this.setState( { entryPrice: value } )

  ChangeStopLossPrice = value => this.setState( { stopLossPrice: value } )

  // Outputs:
  ChangeTargetPrice = value => this.setState( { targetPrice: value } )

  ChangeNumberOfShares = value => this.setState( { numberOfShares: value } )

  ChangeProfitPerShare = value => this.setState( { profitPerShare: value } )

  ChangeStopLossPerShare = value => this.setState( { stopLossPerShare: value } )

  ChangeTotalCost = value => this.setState( { totalCost: value } )
  
  render()
  {
    return(
      <div >

      <Navbar color="light" light expand="md">
      <NavbarBrand href="/">Dragon Journal</NavbarBrand>
          <NavbarToggler onClick={this.toggle} />
          <Collapse isOpen={this.state.isOpen} navbar>
            <Nav className="ml-auto" navbar>
              <NavItem>
                <NavLink href="/components/">Components</NavLink>
              </NavItem>
              <NavItem>
                <NavLink href="https://github.com/reactstrap/reactstrap">GitHub</NavLink>
              </NavItem>
              <UncontrolledDropdown nav inNavbar>
                <DropdownToggle nav caret>
                  Options
                </DropdownToggle>
                <DropdownMenu right>
                  <DropdownItem>
                    Option 1
                  </DropdownItem>
                  <DropdownItem>
                    Option 2
                  </DropdownItem>
                  <DropdownItem divider />
                  <DropdownItem>
                    Reset
                  </DropdownItem>
                </DropdownMenu>
              </UncontrolledDropdown>
            </Nav>
          </Collapse>
      </Navbar>

      <Container>
        <Row>
          <Col sm="4">
            <Row>
              <Col>
                <h3>Inputs:</h3>
                <Row>
                  <Col><Label>Account Size</Label></Col>
                  <Col>
                    <Input 
                      id="AccountSize"
                      type="text"
                      defaultValue={this.state.accountSize}
                      onBlur={e => this.ChangeAccountSize( e.target.value )}
                    />
                  </Col>
                </Row>
                <Row>
                  <Col><Label>Risk Per Trade %</Label></Col>
                  <Col>
                    <Input
                      id="RiskPerTradePercent"
                      type="text"
                      defaultValue={this.state.riskPerTradePercent} 
                      onBlur={e => this.ChangeAccountSize( e.target.value )}
                    />
                  </Col>
                </Row>
                <Row>
                  <Col><Label>Entry Price</Label></Col>
                  <Col>
                    <Input 
                      id="EntryPrice"
                      type="text"
                      defaultValue={this.state.entryPrice}
                      onBlur={e => this.ChangeAccountSize( e.target.value )}
                    />
                  </Col>
                </Row>
                <Row>
                  <Col><Label>Stop Loss Price</Label></Col>
                    <Col>
                      <Input
                        id="StopLossPrice"
                        type="text"
                        defaultValue={this.state.stopLossPrice}
                        onBlur={e => this.ChangeAccountSize( e.target.value )}
                      />
                    </Col>
                </Row>
              </Col>
            </Row>
            <Row>
              <Col>
                <h3>Outputs:</h3>
                <Row>
                  <Col><Label>Target Price</Label></Col>
                  <Col>
                    <Input
                      id="TargetPrice"
                      type="text"
                      value={this.state.targetPrice}
                      onChange={e => this.ChangeAccountSize( e.target.value )}
                    />
                  </Col>
                </Row>
                <Row>
                  <Col><Label>Number of Shares</Label></Col>
                  <Col>
                    <Input
                      id="NumberOfShares"
                      type="text"
                      value={this.state.numberOfShares}
                      onChange={e => this.ChangeNumberOfShares( e.target.value )}
                    />
                  </Col>
                </Row>
                
                <Row>
                  <Col><Label>Profit Per Share</Label></Col>
                  <Col>
                    <Input
                      id="ProfitPerShare"
                      type="text"
                      value={this.state.profitPerShare}
                      onChange={e => this.ChangeProfitePerShare( e.target.value )}
                    />
                  </Col>
                </Row>

                <Row>
                  <Col><Label>Stop Loss Per Share</Label></Col>
                  <Col>
                    <Input
                      id="StopLossPerShare"
                      type="text"
                      value={this.state.stopLossPerShare}
                      onChange={e => this.ChangeStopLossPerShare( e.target.value )}
                    />
                  </Col>
                </Row>

                <Row>
                  <Col><Label>Total Cost:</Label></Col>
                  <Col>
                    <Input
                      id="TotalCost"
                      type="text"
                      value={this.state.totalCost}
                      onChange={e => this.ChangeTotalCost( e.target.value )}
                      disabled
                    />
                  </Col>
                </Row>
              </Col>
            </Row>
            <Row>
              <Col>
                <h3>Constants:</h3>

                <Row>
                  <Col><Label>Return %</Label></Col>
                  <Col>
                    <Input 
                      id="ReturnOnAccountSize"
                      type="text"
                      defaultValue={this.state.returnOnAccountPercent}
                      onBlur={e => this.ChangeAccountSize( e.target.value )}
                    />
                  </Col>
                </Row>
                <Button onClick={this.ComputeValues}>Calculate</Button>
              </Col> 
            </Row>
          </Col>
          <Col sm="8">
            <ChartPanel></ChartPanel>
          </Col>
        </Row>
      </Container>
    </div>
    )
  }
}

export default App;
