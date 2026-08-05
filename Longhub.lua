-- KandaHub - Optimized Graphics & Combat Edition with Custom Background by Miruxz
local Rayfield = loadstring(game:HttpGet('https://sirius.menu/rayfield'))()

local Window = Rayfield:CreateWindow({
   Name = "KandaHub - Ability Arena",
   LoadingTitle = "KandaHub Loading...",
   LoadingSubtitle = "Developer by Miruxz",
   ConfigurationSaving = { Enabled = false },
   KeySystem = false,
   
   -- HÌNH NỀN TÙY CHỈNH CỦA BẠN
   Background = {
      Enabled = true,
      Transparency = 0.3,
      Image = "rbxassetid://111224619797256",
      Color = Color3.fromRGB(0, 30, 80),
   }
})

local CombatTab = Window:CreateTab("Combat Pro", 4483362458)
local MoveTab = Window:CreateTab("Movement", 4483362458)

local Players = game:GetService("Players")
local UserInputService = game:GetService("UserInputService")
local RunService = game:GetService("RunService")
local Lighting = game:GetService("Lighting")
local LocalPlayer = Players.LocalPlayer

getgenv().HitboxEnabled = false
getgenv().TargetLockEnabled = false
getgenv().AntiStunEnabled = false
getgenv().ToggleKey = Enum.KeyCode.Z -- Phím mặc định Z
getgenv().CustomSpeed = 16
getgenv().InfJumpEnabled = false
getgenv().NoclipEnabled = false
getgenv().FullbrightEnabled = false
getgenv().LowGraphicsEnabled = false

-- ==================== COMBAT TAB ====================
CombatTab:CreateToggle({
   Name = "Show Hitbox",
   CurrentValue = false,
   Flag = "HitboxToggle",
   Callback = function(Value)
      getgenv().HitboxEnabled = Value
   end,
})

local TargetLockToggle = CombatTab:CreateToggle({
   Name = "Target lock [Phím Z]",
   CurrentValue = false,
   Flag = "TargetLockToggle",
   Callback = function(Value)
      getgenv().TargetLockEnabled = Value
      if not Value then
          pcall(function()
              local char = LocalPlayer.Character
              if char and char:FindFirstChild("HumanoidRootPart") then
                  char.HumanoidRootPart.AssemblyLinearVelocity = Vector3.new(0, 0, 0)
              end
          end)
      end
   end,
})

CombatTab:CreateInput({
   Name = "Đổi Phím Nhanh (Ghi chữ hoa: Z, J, K, Q)",
   PlaceholderText = "Nhập phím mới...",
   RemoveTextAfterFocusLost = false,
   Flag = "CustomKeyInput",
   Callback = function(Text)
      local success, keycode = pcall(function()
          return Enum.KeyCode[string.upper(Text)]
      end)
      if success and keycode then
          getgenv().ToggleKey = keycode
          Rayfield:Notify({
             Title = "Thành công!",
             Content = "Đã đổi phím bật/tắt thành: " .. string.upper(Text),
             Duration = 3
          })
      end
   end,
})

CombatTab:CreateToggle({
   Name = "Anti Stun & Anti Knockback (Chống choáng & Chống văng)",
   CurrentValue = false,
   Flag = "AntiStunToggle",
   Callback = function(Value)
      getgenv().AntiStunEnabled = Value
   end,
})

-- Xử lý bắt phím trực tiếp
UserInputService.InputBegan:Connect(function(input, gameProcessed)
    if gameProcessed then return end
    
    if input.KeyCode == getgenv().ToggleKey then
        getgenv().TargetLockEnabled = not getgenv().TargetLockEnabled
        TargetLockToggle:Set(getgenv().TargetLockEnabled)
        
        Rayfield:Notify({
           Title = "KandaHub Combat",
           Content = "Target lock: " .. (getgenv().TargetLockEnabled and "BẬT" or "TẮT"),
           Duration = 2
        })
    end
end)

-- Xử lý Show Hitbox (10x10)
RunService.Heartbeat:Connect(function()
    pcall(function()
        if getgenv().HitboxEnabled then
            for _, player in pairs(Players:GetPlayers()) do
                if player ~= LocalPlayer and player.Character and player.Character:FindFirstChild("HumanoidRootPart") then
                    local hrp = player.Character.HumanoidRootPart
                    hrp.Size = Vector3.new(10, 10, 5)
                    hrp.Transparency = 0.75
                    hrp.CanCollide = false
                end
            end
        else
            for _, player in pairs(Players:GetPlayers()) do
                if player ~= LocalPlayer and player.Character and player.Character:FindFirstChild("HumanoidRootPart") then
                    local hrp = player.Character.HumanoidRootPart
                    hrp.Size = Vector3.new(2, 2, 1)
                    hrp.Transparency = 1
                end
            end
        end
    end)
end)

-- Xử lý Target Lock: Tự động dịch chuyển lên trên đỉnh đầu đối thủ gần nhất
RunService.RenderStepped:Connect(function()
    pcall(function()
        if getgenv().TargetLockEnabled then
            local char = LocalPlayer.Character
            if char and char:FindFirstChild("HumanoidRootPart") then
                local myRoot = char.HumanoidRootPart
                local targetRoot = nil
                local shortestDist = 30
                
                for _, player in pairs(Players:GetPlayers()) do
                    if player ~= LocalPlayer and player.Character and player.Character:FindFirstChild("HumanoidRootPart") then
                        local enemyRoot = player.Character.HumanoidRootPart
                        local humanoid = player.Character:FindFirstChild("Humanoid")
                        if humanoid and humanoid.Health > 0 then
                            local dist = (enemyRoot.Position - myRoot.Position).Magnitude
                            if dist < shortestDist then
                                shortestDist = dist
                                targetRoot = enemyRoot
                            end
                        end
                    end
                end
                
                if targetRoot then
                    myRoot.CFrame = targetRoot.CFrame + Vector3.new(0, 4, 0)
                    myRoot.AssemblyLinearVelocity = Vector3.new(0, 0, 0)
                end
            end
        end
    end)
end)

-- Xử lý Anti Stun & Triệt tiêu lực văng
RunService.Heartbeat:Connect(function()
    pcall(function()
        if getgenv().AntiStunEnabled then
            local char = LocalPlayer.Character
            if char and char:FindFirstChild("HumanoidRootPart") then
                local hrp = char.HumanoidRootPart
                
                local vel = hrp.AssemblyLinearVelocity
                if vel.Magnitude > 35 then
                    hrp.AssemblyLinearVelocity = Vector3.new(0, vel.Y > 0 and vel.Y or 0, 0)
                end
                
                for _, v in pairs(char:GetDescendants()) do
                    if v:IsA("BoolValue") or v:IsA("StringValue") then
                        local name = string.lower(v.Name)
                        if name:find("stun") or name:find("ragdoll") or name:find("paralyze") or name:find("freeze") or name:find("down") then
                            v.Value = false
                        end
                    end
                end
                
                local humanoid = char:FindFirstChild("Humanoid")
                if humanoid and humanoid.PlatformStand then
                    humanoid.PlatformStand = false
                end
            end
        end
    end)
end)

-- ==================== MOVEMENT TAB ====================
MoveTab:CreateSlider({
   Name = "WalkSpeed",
   Range = {16, 50},
   Increment = 1,
   Suffix = "Speed",
   CurrentValue = 16,
   Flag = "SpeedSlider",
   Callback = function(Value)
      getgenv().CustomSpeed = Value
   end,
})

RunService.Heartbeat:Connect(function()
    pcall(function()
        if getgenv().CustomSpeed > 16 then
            local char = LocalPlayer.Character
            if char and char:FindFirstChild("Humanoid") and char:FindFirstChild("HumanoidRootPart") then
                local humanoid = char.Humanoid
                local hrp = char.HumanoidRootPart
                if humanoid.MoveDirection.Magnitude > 0 then
                    local speedAdd = (getgenv().CustomSpeed - 16) * 0.05
                    hrp.CFrame = hrp.CFrame + (humanoid.MoveDirection * speedAdd)
                end
            end
        end
    end)
end)

MoveTab:CreateToggle({
   Name = "Infinite Jump (Nhảy vô tận)",
   CurrentValue = false,
   Flag = "InfJumpToggle",
   Callback = function(Value)
      getgenv().InfJumpEnabled = Value
   end,
})

UserInputService.JumpRequest:Connect(function()
    if getgenv().InfJumpEnabled then
        pcall(function()
            local char = LocalPlayer.Character
            if char and char:FindFirstChild("HumanoidRootPart") then
                local hrp = char.HumanoidRootPart
                hrp.AssemblyLinearVelocity = Vector3.new(hrp.AssemblyLinearVelocity.X, 50, hrp.AssemblyLinearVelocity.Z)
            end
        end)
    end
end)

MoveTab:CreateToggle({
   Name = "Safe Noclip (Đi xuyên tường chống rơi)",
   CurrentValue = false,
   Flag = "NoclipToggle",
   Callback = function(Value)
      getgenv().NoclipEnabled = Value
   end,
})

RunService.Stepped:Connect(function()
    pcall(function()
        if getgenv().NoclipEnabled then
            local char = LocalPlayer.Character
            if char and char:FindFirstChild("HumanoidRootPart") then
                for _, part in pairs(char:GetDescendants()) do
                    if part:IsA("BasePart") then
                        if part.Name ~= "HumanoidRootPart" and part.Name ~= "LowerTorso" then
                            part.CanCollide = false
                        end
                    end
                end
            end
        end
    end)
end)

-- Tính năng Fullbright (Tăng độ sáng tối đa)
MoveTab:CreateToggle({
   Name = "Fullbright (Max Brightness)",
   CurrentValue = false,
   Flag = "FullbrightToggle",
   Callback = function(Value)
      getgenv().FullbrightEnabled = Value
   end,
})

RunService.RenderStepped:Connect(function()
    pcall(function()
        if getgenv().FullbrightEnabled then
            Lighting.Brightness = 2
            Lighting.ClockTime = 14
            Lighting.FogEnd = 100000
            Lighting.GlobalShadows = false
        else
            Lighting.GlobalShadows = true
        end
    end)
end)

-- Tính năng Low Graphics (Xóa hiệu ứng đồ họa nặng / Potato Mode)
MoveTab:CreateToggle({
   Name = "Low Graphics (Potato Mode)",
   CurrentValue = false,
   Flag = "LowGraphicsToggle",
   Callback = function(Value)
      getgenv().LowGraphicsEnabled = Value
      if Value then
          pcall(function()
              for _, v in pairs(workspace:GetDescendants()) do
                  if v:IsA("ParticleEmitter") or v:IsA("Trail") or v:IsA("Fire") or v:IsA("Smoke") or v:IsA("Sparkles") then
                      v.Enabled = false
                  end
              end
          end)
      end
   end,
})

Rayfield:LoadConfiguration()
