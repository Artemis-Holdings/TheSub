function get-userInputs {
  # Get Input Network Address
  $inputNetAddr = Read-Host -Prompt "What is the network IPv4 address"
  $inputNetAddr = validateIP -ip $inputNetAddr
  if ($inputNetAddr) {
    $global:db['inputNetAddr'] = $inputNetAddr
  }

  # Get Input Subnet Mask
  $inputSubnetMask = Read-Host -Prompt "What is the mask (255.255.255.192) or CIDR (/24)"
  $inputSubnetMask = validateMask -subnetMask $inputSubnetMask
  if ($inputSubnetMask) {
    $global:db['inputSubnetMask'] = $inputSubnetMask
  }

  # Get N-Nets and Size
  $inputNNets = Read-Host -Prompt "Number of subnets required"
  $global:db['nNets'] = [int]$inputNNets


  # Get Information for subnets
  $subNets = @()
  for ($i=0; $i -lt $global:db['nNets']; $i+=1) {
    $subNetName = Read-Host -Prompt ("Network {0} Common Name" -f ($i+1))
    $subNetSize = [int](Read-Host -Prompt "Number of hosts required")

    #$subnet = @{"net_common_name"=$subNetName;"hosts_req"=$subNetSize}
    #$subnet = validateSubnet -subnet $subnet
    $subnet = validateSubnet -subNetName $subNetName -subNetSize $subNetSize

    if ($subnet) {
      $global:db['subNets'] += $subnet
    }
  }
}

function validateSubnet {
  param(
    [string]$subNetName,
    [int]$subNetSize
  )

  # Check if is nummeric
  try {
    [int]$subNetSize
  } catch {
    write-host "UPDATE: Hosts need to be nummeric. Setting it to minimum size: 4."
    $subNetSize = 4
  }

  # Check minimum Hosts required
  if ($subNetSize -lt 4) {
    write-host "UPDATE: A minimum of 4 hosts is required."
    $subNetSize = 4
  }

  return @{"net_common_name"=$subNetName;"hosts_req"=$subNetSize}
}


function validateMask {
  param(
    [STRING] $subnetMask
  )

  $subnetMaskX = $subnetMask.split('.')

  # Check if is CIDR Notation
  if (($subnetMaskX.count -gt 1) -and (validateIP -ip $subnetMask)) {
    # Check for If is valid IP Format
    write-host "IS valid Subnetmask"
    # Find CIDR
    $sum = 0
    foreach ($octet in $subnetMaskX) {
      $z = [Convert]::ToString($octet,2)
      $x = ($z.ToCharArray() | Where-Object {$_ -eq '1'} | Measure-Object).Count
      $sum += $x
    }
    $subnetMask = $sum
  }
  else {
    $subnetMask = $subnetMask.replace('/','')
  }

  # Check if is Nummeric
  try {
    [INT]$subnetMask
  } catch {
    write-host "ERROR: Subnetmask is not nummeric."
    return $false
  }

  # Check if Mask is <= 32
  if (-not ($subnetMask -gt 32)) {
    write-host "ERROR: Subnetmask is to big."
    return $false
  }

  return $subnetMask
}

function validateIP {
  param(
    [STRING] $ip
  )
  $octets = $ip.split(".")

  # Check IP for Octets
  if (-not ($octets.count -gt 1)) {
    write-host "ERROR: IP too short"
    return $false
  }

  if ($octets.count -gt 4) {
    write-host "ERROR: IP too long"
    return $false
  }

  # Check Size of Octets
  $i = 1
  foreach ($octet in $octets) {
    # Check if Octet is nummeric
    try {
      $octet = [INT]$octet
    } catch {
      write-host "ERROR: Octet $i not nummeric"
      return $false
    }

    # Check Octet Length
    if ($octet -gt 255) {
      write-host "ERROR: Octet $i needs to be 255 or smaller"
      return $false
    }

    $i+=1
  }

  return $octets
}

function get-subnetSize {
  param(
    [int]$reqHosts
  )

  for ($i=0; $i -lt $reqHosts; $i += 1) {
    $x = [Math]::Pow(2, $i)

    if ($x -gt $reqHosts+2) {
      return (32-$i)
    }
  }
}

function find-hosts {
  param(
    [int]$cidr
  )
  $x = 32 - $cidr
  return (([Math]::Pow(2, $x)) - 2)
}

function find-mask {
  param(
    [int] $cidr
  )
  $array_mask = @(255,255,255,255)
  $c = $cidr

  if ($c -lt 8) {
    $w = 32-($c+24)
    #$array_mask[0] = 256 - 2 ** $w
    $array_mask[0] = 256 - ([Math]::Pow(2, $w))
    $array_mask[1] = 0
    $array_mask[2] = 0
    $array_mask[3] = 0
  } else {
    if ($c -lt 16) {
        $x = 32 - ($c + 16)
        $array_mask[0] = 255
        #$array_mask[1] = 256 - (2 ** $x)
        $array_mask[1] = 256 - ([Math]::Pow(2, $x))
        $array_mask[2] = 0
        $array_mask[3] = 0
    } else {
        if ($c -lt 24) {
            $y = 32 - ($c + 8)
            $array_mask[0] = 255
            $array_mask[1] = 255
            #$array_mask[2] = 256 - (2 ** $y)
            $array_mask[2] = 256 - ([Math]::Pow(2, $y))
            $array_mask[3] = 0
        } else {
            $z = 32 - $c
            $array_mask[0] = 255
            $array_mask[1] = 255
            $array_mask[2] = 255
            #$array_mask[3] = 256 - (2 ** $z)
            $array_mask[3] = 256 - ([Math]::Pow(2, $z))
      }
    }
  }
  return $array_mask
}

function find-start {
  param(
    #[int]subnetIDX
    [int[]] $netAddr
  )
  $snNetAddr = @(0,0,0,0)
  if ($netAddr[3] -le 254) {
    $snNetAddr[3] = $netAddr[3] + 1
    $snNetAddr[2] = $netAddr[2]
    $snNetAddr[1] = $netAddr[1]
    $snNetAddr[0] = $netAddr[0]
  }
  elseif ($snNetAddr[2] -le 254) {
    #$snNetAddr[3] = 0
    $snNetAddr[2] = $netAddr[2] + 1
    $snNetAddr[1] = $netAddr[1]
    $snNetAddr[0] = $netAddr[0]
  }
  elseif ($netAddr[1] -le 254) {
    #$snNetAddr[3] = 0
    #$snNetAddr[2] = 0
    $snNetAddr[1] = $netAddr[1] + 1
    $snNetAddr[0] = $netAddr[0]
  }
  else {
    #$snNetAddr[3] = 0
    #$snNetAddr[2] = 0
    #$snNetAddr[1] = 0
    $snNetAddr[0] = $netAddr[1] + 1
  }

  return $snNetAddr
}

function find-wildcard {
  param(
    #[int]subnetIDX
    [int[]] $subMask
  )
  $c = @(1,1,1,1)
  for ($i=0;$i -lt $c.length; $i+=1) {
    $c[$i] = 255 - $subMask[$i]
  }
  return $c
}

function find-broadcast {
  param(
    #[int]subnetIDX
    [int[]] $wildcard,
    [int[]] $netAddr
  )
  $d = @(0,0,0,0)
  for ($i=0;$i -lt $d.length; $i+=1) {
    #$d[$i] = $wildcard[$i] -or $netAddr[$i]
    if ($wildcard[$i] -eq 0) {
      $d[$i] = $netAddr[$i]
    }
    else {
      $d[$i] = $wildcard[$i] + $netAddr[$i]
    }
  }

  return $d
}


function find-end {
  param(
    [int[]] $broadcast
  )
  $snEndAddr = @(0,0,0,0)
  $snEndAddr[3] = $broadcast[3]-1

  for ($i=0; $i -le 2; $i+=1) {
    $snEndAddr[$i] = $broadcast[$i]
  }

  return $snEndAddr
}

function find-net {
  param(
    [int[]] $lastBroadcast
  )
  $net_addr = @(0,0,0,0)
  if ($lastBroadcast[3] -le 254) {
      $net_addr[3] = $lastBroadcast[3] + 1
      $net_addr[2] = $lastBroadcast[2]
      $net_addr[1] = $lastBroadcast[1]
      $net_addr[0] = $lastBroadcast[0]
  }
  elseif ($lastBroadcast[2] -le 254) {
      #$net_addr[3] = int(0)
      $net_addr[2] = $lastBroadcast[2] + 1
      $net_addr[1] = $lastBroadcast[1]
      $net_addr[0] = $lastBroadcast[0]
  }
  elseif ($lastBroadcast[1] -le 254) {
      #$net_addr[3] = int(0)
      #$net_addr[2] = int(0)
      $net_addr[1] = $lastBroadcast[1] + 1
      $net_addr[0] = $lastBroadcast[0]
  }
  else {
      #$net_addr[3] = int(0)
      #$net_addr[2] = int(0)
      #$net_addr[1] = int(0)
      $net_addr[0] = $lastBroadcast[1] + 1
  }

  return $net_addr
}


function calculate-vlsm {
  # Clean Subnets
  $subnets = @()
  foreach ($subnet in $global:db['subNets']) {
    if (-not ($subnet -is [int])) {
      $subnets += $subnet
    }
  }
  $global:db['subNets'] = $subnets

  # Calculate Subnets
  for ($i=0; $i -lt $global:db['subNets'].length; $i+=1) {
    if ($i -eq 0) {
      $global:db['subNets'][$i]['net_add'] = $global:db['inputNetAddr']
      $global:db['subNets'][$i]['cidr'] = (get-subnetSize -reqHosts $global:db['subNets'][$i]['hosts_req'])
      $global:db['subNets'][$i]['hosts_avail'] = (find-hosts -cidr $global:db['subNets'][$i]['cidr'])
      $global:db['subNets'][$i]['hosts_unused'] = $global:db['subNets'][$i]['hosts_avail'] - $global:db['subNets'][$i]['hosts_req']
      $global:db['subNets'][$i]['sub_mask'] = (find-mask -cidr $global:db['subNets'][$i]['cidr'])
      $global:db['subNets'][$i]['sub_delta_r'] = $global:db['subNets'][$i]['hosts_avail'] + 2
      $global:db['subNets'][$i]['sub_start'] = (find-start -netAddr $global:db['subNets'][$i]['net_add'])
      $global:db['subNets'][$i]['sub_wild'] = (find-wildcard -submask $global:db['subNets'][$i]['sub_mask'])
      $global:db['subNets'][$i]['sub_broad'] = (find-broadcast -wildcard $global:db['subNets'][$i]['sub_wild'] -netAddr $global:db['subNets'][$i]['net_add'])
      $global:db['subNets'][$i]['sub_end'] = (find-end -broadcast $global:db['subNets'][$i]['sub_broad'])
    }
    else {
      $global:db['subNets'][$i]['cidr'] = (get-subnetSize -reqHosts $global:db['subNets'][$i]['hosts_req'])
      $global:db['subNets'][$i]['sub_mask'] = (find-mask -cidr $global:db['subNets'][$i]['cidr'])
      $global:db['subNets'][$i]['net_add'] = (find-net -lastBroadcast $global:db['subNets'][$i-1]['sub_broad'])
      $global:db['subNets'][$i]['hosts_avail'] = (find-hosts -cidr $global:db['subNets'][$i]['cidr'])
      $global:db['subNets'][$i]['hosts_unused'] = $global:db['subNets'][$i]['hosts_avail'] - $global:db['subNets'][$i]['hosts_req']
      $global:db['subNets'][$i]['sub_delta_r'] = $global:db['subNets'][$i]['hosts_avail'] + 2
      $global:db['subNets'][$i]['sub_start'] = (find-start -netAddr $global:db['subNets'][$i]['net_add'])
      $global:db['subNets'][$i]['sub_wild'] = (find-wildcard -submask $global:db['subNets'][$i]['sub_mask'])
      $global:db['subNets'][$i]['sub_broad'] = (find-broadcast -wildcard $global:db['subNets'][$i]['sub_wild'] -netAddr $global:db['subNets'][$i]['net_add'])
      $global:db['subNets'][$i]['sub_end'] = (find-end -broadcast $global:db['subNets'][$i]['sub_broad'])
    }

  }
}


function result-print {
  foreach ($subnet in $global:db['subNets']) {
    $subnet | format-table
  }
}

function csv-printer {
  $file = "output.csv"
  $header = @("net_add", "sub_start", "sub_end", "sub_broad",
    "cidr", "sub_mask", "sub_wild",  "hosts_avail",  "hosts_unused",
   "sub_delta_r")

  #set-content -path
  #$fileContent = Import-csv $file -header $header
  $fileContent = @()
  foreach ($subnet in $global:db['subNets']) {
    $newRow = New-Object PsObject -Property @{
      net_add=($subnet['net_add'] -join '.');
      sub_start=($subnet['sub_start'] -join '.');
      sub_end=($subnet['sub_end'] -join '.');
      sub_broad=($subnet['sub_broad'] -join '.');
      cidr=($subnet['cidr']);
      sub_mask=($subnet['sub_mask'] -join '.');
      sub_wild=($subnet['sub_wild'] -join '.');
      hosts_avail=($subnet['hosts_avail']);
      hosts_unused=($subnet['hosts_unused']);
      sub_delta_r=($subnet['sub_delta_r']);
    }
    $fileContent += $newRow
  }

  $outfile = "output.csv"
  $fileContent | Export-CSV -path $outfile -NoTypeInformation -delimiter ':'

  #Format CSV
  $csv = Get-Content $outfile -raw -encoding utf8
  Set-content -path $outfile -value $csv.replace('"','') -encoding utf8


}

################################################################################
# Main
################################################################################
while ($true) {
  try {
    $global:db = @{}
    get-userInputs
    calculate-vlsm

    $global:db['subNets'] | format-list

    result-print
    csv-printer
  }
  catch {
    write-host "ERROR: A global error has occured. Restarting..."
    write-host "STRG+C To exit"
  }
}
