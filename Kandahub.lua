-- Kanda Hub - Pure Black Dark Theme Edition | Developer by Miruxz
local CoreGui = game:GetService("CoreGui")
local Players = game:GetService("Players")
local Workspace = game:GetService("Workspace")
local RunService = game:GetService("RunService")
local UserInputService = game:GetService("UserInputService")
local Lighting = game:GetService("Lighting")
local TweenService = game:GetService("TweenService")
local LocalPlayer = Players.LocalPlayer
local Camera = Workspace.CurrentCamera

-- Dọn dẹp menu cũ
pcall(function()
    if CoreGui:FindFirstChild("KandaHubGui") then
        CoreGui.KandaHubGui:Destroy()
    end
end)

-- Tạo ScreenGui chính
local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Name = "KandaHubGui"
pcall(function() ScreenGui.Parent = CoreGui end)
if not ScreenGui.Parent then ScreenGui.Parent = LocalPlayer:WaitForChild("PlayerGui") end
ScreenGui.ResetOnSpawn = false

-- Khung Main Frame
local MainFrame = Instance.new("Frame")
MainFrame.Size = UDim2.new(0, 680, 0, 440)
MainFrame.Position = UDim2.new(0.5, -340, 0.5, -220)
MainFrame.BackgroundColor3 = Color3.fromRGB(10, 10, 10)
MainFrame.BackgroundTransparency = 0
MainFrame.BorderSizePixel = 0
MainFrame.Active = true
MainFrame.Draggable = true
MainFrame.Parent = ScreenGui

local MainCorner = Instance.new("UICorner")
MainCorner.CornerRadius = UDim.new(0, 10)
MainCorner.Parent = MainFrame

local MainStroke = Instance.new("UIStroke")
MainStroke.Color = Color3.fromRGB(45, 45, 45)
MainStroke.Transparency = 0.2
MainStroke.Thickness = 1.5
MainStroke.Parent = MainFrame

-- Top Bar
local TopBar = Instance.new("Frame")
TopBar.Size = UDim2.new(1, 0, 0, 38)
TopBar.BackgroundColor3 = Color3.fromRGB(15, 15, 15)
TopBar.BackgroundTransparency = 0
TopBar.BorderSizePixel = 0
TopBar.ZIndex = 2
TopBar.Parent = MainFrame

local TopCorner = Instance.new("UICorner")
TopCorner.CornerRadius = UDim.new(0, 10)
TopCorner.Parent = TopBar

local TitleLabel = Instance.new("TextLabel")
TitleLabel.Size = UDim2.new(1, -70, 1, 0)
TitleLabel.Position = UDim2.new(0, 15, 0, 0)
TitleLabel.BackgroundTransparency = 1
TitleLabel.Text = "Kanda Hub | Developer by Miruxz"
TitleLabel.TextColor3 = Color3.fromRGB(255, 255, 255)
TitleLabel.TextSize = 12
TitleLabel.Font = Enum.Font.GothamBold
TitleLabel.TextXAlignment = Enum.TextXAlignment.Left
TitleLabel.ZIndex = 3
TitleLabel.Parent = TopBar

local ContainerBody = Instance.new("Frame")
ContainerBody.Size = UDim2.new(1, 0, 1, -38)
ContainerBody.Position = UDim2.new(0, 0, 0, 38)
ContainerBody.BackgroundTransparency = 1
ContainerBody.ZIndex = 2
ContainerBody.Parent = MainFrame

local Sidebar = Instance.new("ScrollingFrame")
Sidebar.Size = UDim2.new(0, 155, 1, -8)
Sidebar.Position = UDim2.new(0, 8, 0, 4)
Sidebar.BackgroundColor3 = Color3.fromRGB(18, 18, 18)
Sidebar.BackgroundTransparency = 0
Sidebar.BorderSizePixel = 0
Sidebar.CanvasSize = UDim2.new(0, 0, 0, 0)
Sidebar.ScrollBarThickness = 2
Sidebar.ScrollBarImageColor3 = Color3.fromRGB(70, 70, 70)
Sidebar.ZIndex = 3
Sidebar.Parent = ContainerBody

local SidebarCorner = Instance.new("UICorner")
SidebarCorner.CornerRadius = UDim.new(0, 8)
SidebarCorner.Parent = Sidebar

local SidebarLayout = Instance.new("UIListLayout")
SidebarLayout.SortOrder = Enum.SortOrder.LayoutOrder
SidebarLayout.Padding = UDim.new(0, 5)
SidebarLayout.Parent = Sidebar

local ContentArea = Instance.new("Frame")
ContentArea.Size = UDim2.new(1, -178, 1, -8)
ContentArea.Position = UDim2.new(0, 168, 0, 4)
ContentArea.BackgroundColor3 = Color3.fromRGB(15, 15, 15)
ContentArea.BackgroundTransparency = 0
ContentArea.BorderSizePixel = 0
ContentArea.ZIndex = 3
ContentArea.Parent = ContainerBody

local ContentCorner = Instance.new("UICorner")
ContentCorner.CornerRadius = UDim.new(0, 8)
ContentCorner.Parent = ContentArea

-- Nút Thu Gọn (-)
local MinBtn = Instance.new("TextButton")
MinBtn.Size = UDim2.new(0, 26, 0, 26)
MinBtn.Position = UDim2.new(1, -62, 0, 6)
MinBtn.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
MinBtn.Text = "-"
MinBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
MinBtn.TextSize = 16
MinBtn.Font = Enum.Font.GothamBold
MinBtn.ZIndex = 4
MinBtn.Parent = TopBar

local MinCorner = Instance.new("UICorner")
MinCorner.CornerRadius = UDim.new(0, 6)
MinCorner.Parent = MinBtn

-- Nút Tắt (X)
local CloseBtn = Instance.new("TextButton")
CloseBtn.Size = UDim2.new(0, 26, 0, 26)
CloseBtn.Position = UDim2.new(1, -32, 0, 6)
CloseBtn.BackgroundColor3 = Color3.fromRGB(180, 40, 40)
CloseBtn.Text = "X"
CloseBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
CloseBtn.TextSize = 12
CloseBtn.Font = Enum.Font.GothamBold
CloseBtn.ZIndex = 4
CloseBtn.Parent = TopBar

local CloseCorner = Instance.new("UICorner")
CloseCorner.CornerRadius = UDim.new(0, 6)
CloseCorner.Parent = CloseBtn

local isMinimized = false
MinBtn.MouseButton1Click:Connect(function()
    isMinimized = not isMinimized
    if isMinimized then
        MinBtn.Text = "+"
        ContainerBody.Visible = false
        TweenService:Create(MainFrame, TweenInfo.new(0.2), {Size = UDim2.new(0, 680, 0, 38)}):Play()
    else
        MinBtn.Text = "-"
        ContainerBody.Visible = true
        TweenService:Create(MainFrame, TweenInfo.new(0.2), {Size = UDim2.new(0, 680, 0, 440)}):Play()
    end
end)

CloseBtn.MouseButton1Click:Connect(function()
    ScreenGui:Destroy()
end)

UserInputService.InputBegan:Connect(function(input, gameProcessed)
    if not gameProcessed and input.KeyCode == Enum.KeyCode.Insert then
        MainFrame.Visible = not MainFrame.Visible
    end
end)

local Tabs = {}
local CurrentTab = nil

local function createTab(name)
    local tabContainer = Instance.new("ScrollingFrame")
    tabContainer.Size = UDim2.new(1, -16, 1, -16)
    tabContainer.Position = UDim2.new(0, 8, 0, 8)
    tabContainer.BackgroundTransparency = 1
    tabContainer.CanvasSize = UDim2.new(0, 0, 2, 0)
    tabContainer.ScrollBarThickness = 3
    tabContainer.ScrollBarImageColor3 = Color3.fromRGB(70, 70, 70)
    tabContainer.Visible = false
    tabContainer.ZIndex = 4
    tabContainer.Parent = ContentArea

    local tabLayout = Instance.new("UIListLayout")
    tabLayout.SortOrder = Enum.SortOrder.LayoutOrder
    tabLayout.Padding = UDim.new(0, 8)
    tabLayout.Parent = tabContainer

    local tabBtn = Instance.new("TextButton")
    tabBtn.Size = UDim2.new(1, -10, 0, 36)
    tabBtn.Position = UDim2.new(0, 5, 0, 0)
    tabBtn.BackgroundColor3 = Color3.fromRGB(26, 26, 26)
    tabBtn.BackgroundTransparency = 0
    tabBtn.Text = "   " .. name
    tabBtn.TextColor3 = Color3.fromRGB(160, 160, 160)
    tabBtn.TextSize = 13
    tabBtn.Font = Enum.Font.GothamMedium
    tabBtn.TextXAlignment = Enum.TextXAlignment.Left
    tabBtn.ZIndex = 4
    tabBtn.Parent = Sidebar

    local btnCorner = Instance.new("UICorner")
    btnCorner.CornerRadius = UDim.new(0, 6)
    btnCorner.Parent = tabBtn

    tabBtn.MouseButton1Click:Connect(function()
        for _, t in pairs(Tabs) do
            t.Container.Visible = false
            TweenService:Create(t.Button, TweenInfo.new(0.2), {BackgroundColor3 = Color3.fromRGB(26, 26, 26), TextColor3 = Color3.fromRGB(160, 160, 160)}):Play()
        end
        tabContainer.Visible = true
        TweenService:Create(tabBtn, TweenInfo.new(0.2), {BackgroundColor3 = Color3.fromRGB(45, 45, 45), TextColor3 = Color3.fromRGB(255, 255, 255)}):Play()
    end)

    if not CurrentTab then
        tabContainer.Visible = true
        tabBtn.BackgroundColor3 = Color3.fromRGB(45, 45, 45)
        tabBtn.TextColor3 = Color3.fromRGB(255, 255, 255)
        CurrentTab = tabContainer
    end

    table.insert(Tabs, {Container = tabContainer, Button = tabBtn})
    return tabContainer
end

local TabInfo = createTab("Info")
local TabMain = createTab("Main")
local TabCombat = createTab("Combat")
local TabVisuals = createTab("Visuals")
local TabPlayer = createTab("Player")

local TogglesTable = {}

local function createToggle(tab, name, callback)
    local btn = Instance.new("TextButton")
    btn.Size = UDim2.new(1, 0, 0, 38)
    btn.BackgroundColor3 = Color3.fromRGB(22, 22, 22)
    btn.BackgroundTransparency = 0
    btn.Text = "   [ OFF ]    " .. name
    btn.TextColor3 = Color3.fromRGB(180, 180, 180)
    btn.TextSize = 13
    btn.Font = Enum.Font.GothamMedium
    btn.TextXAlignment = Enum.TextXAlignment.Left
    btn.ZIndex = 5
    btn.Parent = tab

    local corner = Instance.new("UICorner")
    corner.CornerRadius = UDim.new(0, 6)
    corner.Parent = btn
    
    local stroke = Instance.new("UIStroke")
    stroke.Color = Color3.fromRGB(50, 50, 50)
    stroke.Transparency = 0.5
    stroke.Thickness = 1
    stroke.Parent = btn

    local state = false
    local function updateState(newState)
        state = newState
        if state then
            btn.Text = "   [ ON ]     " .. name
            TweenService:Create(btn, TweenInfo.new(0.2), {BackgroundColor3 = Color3.fromRGB(45, 45, 45), TextColor3 = Color3.fromRGB(255, 255, 255)}):Play()
        else
            btn.Text = "   [ OFF ]    " .. name
            TweenService:Create(btn, TweenInfo.new(0.2), {BackgroundColor3 = Color3.fromRGB(22, 22, 22), TextColor3 = Color3.fromRGB(180, 180, 180)}):Play()
        end
        callback(state)
    end

    btn.MouseButton1Click:Connect(function()
        updateState(not state)
    end)

    if name:find("Aimbot") then
        TogglesTable.Aimbot = {Set = updateState, Get = function() return state end}
    end
end

local function createSlider(tab, name, min, max, default, callback)
    local frame = Instance.new("Frame")
    frame.Size = UDim2.new(1, 0, 0, 56)
    frame.BackgroundColor3 = Color3.fromRGB(22, 22, 22)
    frame.BackgroundTransparency = 0
    frame.ZIndex = 5
    frame.Parent = tab

    local corner = Instance.new("UICorner")
    corner.CornerRadius = UDim.new(0, 6)
    corner.Parent = frame

    local label = Instance.new("TextLabel")
    label.Size = UDim2.new(1, -15, 0, 24)
    label.Position = UDim2.new(0, 10, 0, 4)
    label.BackgroundTransparency = 1
    label.Text = name .. ": " .. default
    label.TextColor3 = Color3.fromRGB(200, 200, 200)
    label.TextSize = 13
    label.Font = Enum.Font.GothamMedium
    label.TextXAlignment = Enum.TextXAlignment.Left
    label.ZIndex = 6
    label.Parent = frame

    local sliderBg = Instance.new("Frame")
    sliderBg.Size = UDim2.new(1, -20, 0, 8)
    sliderBg.Position = UDim2.new(0, 10, 0, 36)
    sliderBg.BackgroundColor3 = Color3.fromRGB(35, 35, 35)
    sliderBg.BorderSizePixel = 0
    sliderBg.ZIndex = 6
    sliderBg.Parent = frame

    local sliderBgCorner = Instance.new("UICorner")
    sliderBgCorner.CornerRadius = UDim.new(0, 4)
    sliderBgCorner.Parent = sliderBg

    local sliderFill = Instance.new("Frame")
    sliderFill.Size = UDim2.new((default - min) / (max - min), 0, 1, 0)
    sliderFill.BackgroundColor3 = Color3.fromRGB(255, 50, 50)
    sliderFill.BorderSizePixel = 0
    sliderFill.ZIndex = 7
    sliderFill.Parent = sliderBg

    local sliderFillCorner = Instance.new("UICorner")
    sliderFillCorner.CornerRadius = UDim.new(0, 4)
    sliderFillCorner.Parent = sliderFill

    local dragging = false
    local function updateInput(input)
        local pos = math.clamp((input.Position.X - sliderBg.AbsolutePosition.X) / sliderBg.AbsoluteSize.X, 0, 1)
        local val = math.floor(min + (max - min) * pos)
        sliderFill.Size = UDim2.new(pos, 0, 1, 0)
        label.Text = name .. ": " .. val
        callback(val)
    end

    sliderBg.InputBegan:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
            dragging = true
            updateInput(input)
        end
    end)

    UserInputService.InputEnded:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
            dragging = false
        end
    end)

    UserInputService.InputChanged:Connect(function(input)
        if dragging and (input.UserInputType == Enum.UserInputType.MouseMovement or input.UserInputType == Enum.UserInputType.Touch) then
            updateInput(input)
        end
    end)
end

-- Tab Info Content
local InfoLabel = Instance.new("TextLabel")
InfoLabel.Size = UDim2.new(1, 0, 0, 120)
InfoLabel.BackgroundTransparency = 1
InfoLabel.Text = "Kanda Hub Pure Black Edition\nDeveloper: Miruxz\nStatus: Connected Successfully\n[Insert]: Toggle Menu | [Press E]: Toggle Aimbot On/Off."
InfoLabel.TextColor3 = Color3.fromRGB(220, 220, 220)
InfoLabel.TextSize = 13
InfoLabel.Font = Enum.Font.GothamSemibold
InfoLabel.TextXAlignment = Enum.TextXAlignment.Left
InfoLabel.TextYAlignment = Enum.TextYAlignment.Top
InfoLabel.ZIndex = 5
InfoLabel.Parent = TabInfo

-- ==================== TAB MAIN (AUTO FARM CRYSTAL / SHARD) ====================
getgenv().AutoShard = false
getgenv().ShardRange = 300

createToggle(TabMain, "Auto Farm Crystal", function(state)
    getgenv().AutoShard = state
    task.spawn(function()
        while getgenv().AutoShard do
            pcall(function()
                local char = LocalPlayer.Character
                if char and char:FindFirstChild("HumanoidRootPart") then
                    local hrp = char.HumanoidRootPart
                    local foundTarget = false
                    
                    for _, obj in pairs(Workspace:GetDescendants()) do
                        if not getgenv().AutoShard then break end
                        
                        local targetPart = nil
                        local nameLower = string.lower(obj.Name)
                        
                        if nameLower:find("shard") or nameLower:find("token") or nameLower:find("crystal") or nameLower:find("coin") or nameLower:find("gem") or nameLower:find("drop") or nameLower:find("pickup") then
                            if obj:IsA("Model") then
                                targetPart = obj.PrimaryPart or obj:FindFirstChildWhichIsA("BasePart", true)
                            elseif obj:IsA("BasePart") and not obj:IsDescendantOf(Players) then
                                targetPart = obj
                            end
                            
                            if targetPart then
                                local dist = (hrp.Position - targetPart.Position).Magnitude
                                if dist <= getgenv().ShardRange then
                                    foundTarget = true
                                    hrp.CFrame = targetPart.CFrame + Vector3.new(0, 1, 0)
                                    task.wait(0.2)
                                    break
                                end
                            end
                        end
                    end
                    
                    if not foundTarget then
                        task.wait(0.4)
                    end
                end
            end)
            task.wait(0.1)
        end
    end)
end)

createSlider(TabMain, "Crystal Range (Studs)", 50, 1000, 300, function(value)
    getgenv().ShardRange = value
end)

-- ==================== TAB COMBAT ====================
getgenv().AimLockActive = false

createToggle(TabCombat, "Aimbot", function(state)
    getgenv().AimLockActive = state
end)

-- Phím E: Bấm để bật / Bấm lần nữa để tắt
UserInputService.InputBegan:Connect(function(input, gameProcessed)
    if not gameProcessed and input.KeyCode == Enum.KeyCode.E then
        getgenv().AimLockActive = not getgenv().AimLockActive
        if TogglesTable.Aimbot then 
            TogglesTable.Aimbot.Set(getgenv().AimLockActive) 
        end
    end
end)

local FOVCircle = Drawing.new("Circle")
FOVCircle.Visible = false
FOVCircle.ZIndex = 999
FOVCircle.Transparency = 0.8
FOVCircle.Color = Color3.fromRGB(255, 255, 255)
FOVCircle.Thickness = 1.5
FOVCircle.NumSides = 64
FOVCircle.Radius = 150
FOVCircle.Filled = false

RunService.RenderStepped:Connect(function()
    FOVCircle.Position = UserInputService:GetMouseLocation()
    if getgenv().AimLockActive then
        pcall(function()
            local hrpLocal = LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("HumanoidRootPart")
            if not hrpLocal then return end
            
            local targetPart = nil
            local shortestDist = math.huge
            
            for _, p in pairs(Players:GetPlayers()) do
                if p ~= LocalPlayer and p.Character then
                    local humanoid = p.Character:FindFirstChildOfClass("Humanoid")
                    local head = p.Character:FindFirstChild("Head") or p.Character:FindFirstChild("HumanoidRootPart")
                    
                    if humanoid and humanoid.Health > 0 and head then
                        local screenPoint, onScreen = Camera:WorldToViewportPoint(head.Position)
                        local mousePos = UserInputService:GetMouseLocation()
                        local distToMouse = (Vector2.new(screenPoint.X, screenPoint.Y) - mousePos).Magnitude
                        
                        if distToMouse <= FOVCircle.Radius then
                            local dist3D = (hrpLocal.Position - head.Position).Magnitude
                            if dist3D < shortestDist then
                                shortestDist = dist3D
                                targetPart = head
                            end
                        end
                    end
                end
            end
            
            if targetPart then
                Camera.CFrame = CFrame.new(Camera.CFrame.Position, targetPart.Position)
            end
        end)
    end
end)

createToggle(TabCombat, "FOV Circle", function(state)
    FOVCircle.Visible = state
end)

getgenv().HitboxEnabled = false
getgenv().HitboxSize = 6

createToggle(TabCombat, "Hitbox Expander", function(state)
    getgenv().HitboxEnabled = state
end)

createSlider(TabCombat, "Hitbox Size", 1, 50, 6, function(value)
    getgenv().HitboxSize = value
end)

RunService.RenderStepped:Connect(function()
    if getgenv().HitboxEnabled then
        pcall(function()
            for _, p in pairs(Players:GetPlayers()) do
                if p ~= LocalPlayer and p.Character and p.Character:FindFirstChild("HumanoidRootPart") then
                    local hrp = p.Character.HumanoidRootPart
                    hrp.Size = Vector3.new(getgenv().HitboxSize, getgenv().HitboxSize, getgenv().HitboxSize)
                    hrp.Transparency = 0.5
                    hrp.Color = Color3.fromRGB(255, 0, 0)
                    hrp.Material = Enum.Material.Neon
                    hrp.CanCollide = false
                end
            end
        end)
    end
end)

-- ==================== TAB VISUALS ====================
getgenv().TracingLine = false
createToggle(TabVisuals, "Tracing Lines", function(state)
    getgenv().TracingLine = state
end)

local tracers = {}
RunService.RenderStepped:Connect(function()
    pcall(function()
        if not getgenv().TracingLine then
            for _, line in pairs(tracers) do
                line.Visible = false
            end
            return
        end
        
        for _, player in pairs(Players:GetPlayers()) do
            if player ~= LocalPlayer and player.Character and player.Character:FindFirstChild("HumanoidRootPart") then
                local hrp = player.Character.HumanoidRootPart
                local vector, onScreen = Camera:WorldToViewportPoint(hrp.Position)
                
                if not tracers[player] then
                    local line = Drawing.new("Line")
                    line.Thickness = 1.5
                    line.Color = Color3.fromRGB(255, 50, 50)
                    line.Transparency = 0.7
                    tracers[player] = line
                end
                
                local line = tracers[player]
                if onScreen then
                    line.From = Vector2.new(Camera.ViewportSize.X / 2, Camera.ViewportSize.Y)
                    line.To = Vector2.new(vector.X, vector.Y)
                    line.Visible = true
                else
                    line.Visible = false
                end
            end
        end
    end)
end)

getgenv().Fullbright = false
createToggle(TabVisuals, "Fullbright", function(state)
    getgenv().Fullbright = state
end)

RunService.RenderStepped:Connect(function()
    if getgenv().Fullbright then
        Lighting.Brightness = 2
        Lighting.ClockTime = 14
        Lighting.GlobalShadows = false
        Lighting.OutdoorAmbient = Color3.fromRGB(200, 200, 200)
    else
        Lighting.Brightness = 1
        Lighting.GlobalShadows = true
        Lighting.OutdoorAmbient = Color3.fromRGB(128, 128, 128)
    end
end)

-- ==================== TAB PLAYER ====================
local AntiFling = true
createToggle(TabPlayer, "Anti-Fling", function(state)
    AntiFling = state
end)

RunService.Stepped:Connect(function()
    if AntiFling then
        pcall(function()
            for _, p in pairs(Players:GetPlayers()) do
                if p ~= LocalPlayer and p.Character and p.Character:FindFirstChild("HumanoidRootPart") then
                    p.Character.HumanoidRootPart.Velocity = Vector3.new(0, 0, 0)
                end
            end
        end)
    end
end)
