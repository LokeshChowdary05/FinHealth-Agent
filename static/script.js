// JavaScript for FinHealth Bot Interactions

document.addEventListener('DOMContentLoaded', (event) => {
    const chatMessages = document.querySelector('#chatMessages');
    const chatInput = document.querySelector('#chatInput');
    const sendButton = document.querySelector('#sendButton');
    const loadingIndicator = document.querySelector('#loadingIndicator');
    const initialForm = document.querySelector('#initialForm');
    const formLocation = document.querySelector('#formLocation');
    const formProcedure = document.querySelector('#formProcedure');
    const formInsurance = document.querySelector('#formInsurance');

    // Initially hide chatbot until form submission
    chatMessages.style.display = 'none';

    // Form submission handler
    initialForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        const location = formLocation.value.trim();
        const procedure = formProcedure.value;
        const insurance = formInsurance.value.trim();

        // Handle initial form submission logic here
        await handleFormSubmission(location, procedure, insurance);

        // Show chatbot messages
        initialForm.style.display = 'none';
        chatMessages.style.display = 'block';
    });

    async function handleFormSubmission(location, procedure, insurance) {
        // In a real implementation, you might store this information in the server
        console.log('Form submitted with:', { location, procedure, insurance });
        renderBotMessage('Thank you! You provided the following details:');
        renderBotMessage(`Location: ${location}`);
        renderBotMessage(`Procedure: ${procedure}`);
        if (insurance) {
            renderBotMessage(`Insurance: ${insurance}`);
        } else {
            renderBotMessage(`Insurance: Not provided`);
        }
    }

    // Send message
    async function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;

        renderUserMessage(message);
        chatInput.value = '';
        chatInput.focus();

        // Show loading
        showLoading();

        try {
            await processMessage(message);
        } catch (error) {
            console.error('Error processing message:', error);
            renderBotMessage('Sorry, I encountered an error. Please try again.');
        } finally {
            hideLoading();
        }
    }

    // Render user message
    function renderUserMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message user-message';
        messageElement.innerHTML = `
            <div class="message-avatar">👤</div>
            <div class="message-content">${escapeHtml(message)}</div>
        `;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Process message with enhanced conversation manager
    async function processMessage(message) {
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    context: {}
                })
            });
            
            const data = await response.json();
            if (data.response) {
                await handleConversationResponse(data.response, message);
            } else {
                renderBotMessage('I\'m here to help you save money on healthcare! What would you like to know?');
            }
        } catch (error) {
            console.error('Error processing message:', error);
            renderBotMessage('Sorry, I encountered an error. Please try again.');
        }
    }

    // Handle different conversation response types
    async function handleConversationResponse(response, originalMessage) {
        const responseType = response.type;
        
        switch (responseType) {
            case 'direct_price_analysis':
            case 'price_comparison':
            case 'complete_analysis':
                renderProfessionalAnalysis(response);
                break;
                
            case 'symptom_analysis':
                renderSymptomAnalysis(response);
                break;
                
            case 'detailed_comparison':
                renderDetailedComparison(response);
                break;
                
            case 'hospital_list':
                renderHospitalList(response);
                break;
                
            case 'insurance_details':
                renderInsuranceDetails(response);
                break;
                
            case 'procedure_info':
                renderProcedureInfo(response);
                break;
                
            case 'procedure_location_request':
                renderProcedureLocationRequest(response);
                break;
                
            case 'procedure_location_analysis':
                renderProcedureLocationAnalysis(response);
                break;
                
            case 'insurance_form_request':
                renderInsuranceFormRequest(response);
                break;
                
            case 'insurance_location_request':
                renderInsuranceLocationRequest(response);
                break;
                
            case 'insurance_location_analysis':
                renderInsuranceLocationAnalysis(response);
                break;
                
            case 'emergency_info':
                renderEmergencyInfo(response);
                break;
                
            case 'general_assistance':
                renderGeneralAssistance(response);
                break;
                
            default:
                renderBotMessage(response.message);
                if (response.suggestions) {
                    renderSuggestions(response.suggestions);
                }
                break;
        }
    }

    // Analyze symptoms
    async function analyzeSymptoms(symptoms) {
        try {
            const response = await fetch('/api/analyze-symptoms', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ symptoms: symptoms })
            });
            
            const data = await response.json();
            if (data.condition && data.procedures) {
                let message = `Based on your symptoms, you might be experiencing **${data.condition}**.\n\n`;
                message += `Recommended procedures:\n`;
                data.procedures.forEach(proc => {
                    message += `• ${proc}\n`;
                });
                message += `\nWould you like me to compare prices for these procedures at nearby hospitals?`;
                renderBotMessage(message);
            } else {
                renderBotMessage('I\'m analyzing your symptoms. Please consult with a healthcare professional for proper diagnosis.');
            }
        } catch (error) {
            renderBotMessage('Sorry, I couldn\'t analyze your symptoms right now. Please try again.');
        }
    }

    // Compare hospital prices
    async function compareHospitalPrices(query) {
        // Extract procedures from query (simplified)
        const procedures = extractProcedures(query);
        const location = extractLocation(query) || 'New York';
        
        try {
            const response = await fetch('/api/compare-hospitals', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    procedures: procedures,
                    location: location
                })
            });
            
            const data = await response.json();
            if (data.hospitals && data.hospitals.length > 0) {
                renderHospitalComparison(data.hospitals, procedures);
            } else {
                renderBotMessage('I couldn\'t find hospital pricing data for those procedures. Please try specifying common procedures like ECG, X-ray, MRI, or Blood tests.');
            }
        } catch (error) {
            renderBotMessage('Sorry, I couldn\'t compare hospital prices right now. Please try again.');
        }
    }

    // Analyze insurance coverage
    async function analyzeInsurance(query) {
        // This is a simplified implementation
        const insurancePlans = ['Aetna', 'Blue Cross Blue Shield', 'Cigna', 'UnitedHealth', 'Medicare', 'Medicaid'];
        let message = 'I can analyze insurance coverage for the following plans:\n\n';
        insurancePlans.forEach(plan => {
            message += `• ${plan}\n`;
        });
        message += '\nPlease specify your insurance plan and the procedures you need, and I\'ll calculate your costs.';
        renderBotMessage(message);
    }

    // Extract procedures from query (simplified)
    function extractProcedures(query) {
        const commonProcedures = ['ECG', 'X-ray', 'MRI', 'CT scan', 'Blood tests', 'Ultrasound', 'Physical examination', 'Stress test'];
        const found = [];
        const lowerQuery = query.toLowerCase();
        
        commonProcedures.forEach(proc => {
            if (lowerQuery.includes(proc.toLowerCase())) {
                found.push(proc);
            }
        });
        
        // Default procedures if none found
        if (found.length === 0) {
            if (lowerQuery.includes('chest') || lowerQuery.includes('heart')) {
                return ['ECG', 'Chest X-ray'];
            } else if (lowerQuery.includes('blood')) {
                return ['Blood tests'];
            } else {
                return ['Physical examination'];
            }
        }
        
        return found;
    }

    // Extract location from query - supports all US cities including Lubbock
    function extractLocation(query) {
        const lowerQuery = query.toLowerCase();
        
        // Comprehensive city mapping
        const cityMap = {
            // Texas cities including Lubbock
            'lubbock': 'Lubbock', 'houston': 'Houston', 'dallas': 'Dallas', 'austin': 'Austin',
            'san antonio': 'San Antonio', 'fort worth': 'Fort Worth', 'el paso': 'El Paso',
            'arlington': 'Arlington', 'corpus christi': 'Corpus Christi', 'plano': 'Plano',
            'texas': 'Houston',
            
            // Major cities from all states
            'new york': 'New York', 'nyc': 'New York', 'manhattan': 'New York', 'brooklyn': 'New York',
            'los angeles': 'Los Angeles', 'la': 'Los Angeles', 'hollywood': 'Los Angeles',
            'chicago': 'Chicago', 'illinois': 'Chicago',
            'miami': 'Miami', 'florida': 'Miami',
            'boston': 'Boston', 'massachusetts': 'Boston',
            'atlanta': 'Atlanta', 'georgia': 'Atlanta',
            'seattle': 'Seattle', 'washington': 'Seattle',
            'phoenix': 'Phoenix', 'arizona': 'Phoenix',
            'philadelphia': 'Philadelphia', 'denver': 'Denver', 'detroit': 'Detroit',
            'columbus': 'Columbus', 'charlotte': 'Charlotte', 'memphis': 'Memphis',
            'baltimore': 'Baltimore', 'milwaukee': 'Milwaukee', 'albuquerque': 'Albuquerque',
            'tucson': 'Tucson', 'fresno': 'Fresno', 'sacramento': 'Sacramento',
            'kansas city': 'Kansas City', 'mesa': 'Mesa', 'virginia beach': 'Virginia Beach',
            'omaha': 'Omaha', 'colorado springs': 'Colorado Springs', 'raleigh': 'Raleigh',
            'long beach': 'Long Beach', 'miami beach': 'Miami', 'virginia beach': 'Virginia Beach',
            'oakland': 'Oakland', 'minneapolis': 'Minneapolis', 'tulsa': 'Tulsa',
            'cleveland': 'Cleveland', 'wichita': 'Wichita', 'arlington': 'Arlington',
            'new orleans': 'New Orleans', 'bakersfield': 'Bakersfield', 'tampa': 'Tampa',
            'honolulu': 'Honolulu', 'anaheim': 'Anaheim', 'santa ana': 'Santa Ana',
            'corpus christi': 'Corpus Christi', 'riverside': 'Riverside', 'lexington': 'Lexington',
            'stockton': 'Stockton', 'saint paul': 'Saint Paul', 'cincinnati': 'Cincinnati',
            'anchorage': 'Anchorage', 'henderson': 'Henderson', 'greensboro': 'Greensboro',
            'plano': 'Plano', 'newark': 'Newark', 'lincoln': 'Lincoln', 'buffalo': 'Buffalo',
            'jersey city': 'Jersey City', 'chula vista': 'Chula Vista', 'fort wayne': 'Fort Wayne',
            'orlando': 'Orlando', 'st. petersburg': 'St. Petersburg', 'chandler': 'Chandler',
            'laredo': 'Laredo', 'norfolk': 'Norfolk', 'durham': 'Durham', 'madison': 'Madison',
            'lubbock': 'Lubbock', 'irvine': 'Irvine', 'winston-salem': 'Winston-Salem',
            'glendale': 'Glendale', 'garland': 'Garland', 'hialeah': 'Hialeah',
            'reno': 'Reno', 'chesapeake': 'Chesapeake', 'gilbert': 'Gilbert',
            'baton rouge': 'Baton Rouge', 'irving': 'Irving', 'scottsdale': 'Scottsdale',
            'north las vegas': 'North Las Vegas', 'fremont': 'Fremont', 'boise': 'Boise',
            'richmond': 'Richmond', 'san bernardino': 'San Bernardino', 'birmingham': 'Birmingham',
            'spokane': 'Spokane', 'rochester': 'Rochester', 'des moines': 'Des Moines',
            'modesto': 'Modesto', 'fayetteville': 'Fayetteville', 'tacoma': 'Tacoma',
            'oxnard': 'Oxnard', 'fontana': 'Fontana', 'columbus': 'Columbus',
            'montgomery': 'Montgomery', 'moreno valley': 'Moreno Valley', 'akron': 'Akron',
            'yonkers': 'Yonkers', 'aurora': 'Aurora', 'huntington beach': 'Huntington Beach'
        };
        
        // Find the longest matching city name for better accuracy
        let bestMatch = null;
        let longestMatch = 0;
        
        for (const [cityKey, cityName] of Object.entries(cityMap)) {
            if (lowerQuery.includes(cityKey) && cityKey.length > longestMatch) {
                bestMatch = cityName;
                longestMatch = cityKey.length;
            }
        }
        
        return bestMatch;
    }

    // Render hospital comparison results
    function renderHospitalComparison(hospitals, procedures) {
        const hospitalTable = createHospitalComparisonTable(hospitals, procedures);
        renderBotMessageWithTable(`🏥 **Hospital Price Comparison** for ${procedures.join(', ')}:`, hospitalTable);
    }

    // Create hospital comparison table
    function createHospitalComparisonTable(hospitals, procedures) {
        let tableHTML = `
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Hospital</th>
                        <th>Rating</th>
                        <th>Wait Time</th>
                        <th>Total Cost</th>
                        <th>Cash Price</th>
                        <th>Savings</th>
                        <th>Emergency</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        hospitals.forEach((hospital, index) => {
            const hospitalInfo = hospital.hospital;
            const emergency = hospitalInfo.emergency ? '✅ Yes' : '❌ No';
            
            tableHTML += `
                <tr>
                    <td>
                        <strong>${hospitalInfo.name}</strong><br>
                        <small style="color: #999;">${hospitalInfo.address}</small><br>
                        <small style="color: #999;">📞 ${hospitalInfo.phone}</small>
                    </td>
                    <td class="rating-cell">⭐ ${hospitalInfo.rating}/5</td>
                    <td>${hospital.estimated_wait_time}</td>
                    <td class="price-cell">$${hospital.total_cost}</td>
                    <td class="price-cell">$${hospital.total_cash_cost}</td>
                    <td class="savings-cell">$${hospital.total_savings_cash}</td>
                    <td>${emergency}</td>
                </tr>
            `;
        });
        
        tableHTML += `
                </tbody>
            </table>
            <div style="margin-top: 1rem; padding: 0.75rem; background: rgba(255,255,255,0.05); border-radius: 0.5rem;">
                💡 <strong>Best Value:</strong> ${hospitals[0].hospital.name} offers the lowest total cost at $${hospitals[0].total_cash_cost} (cash price)
            </div>
        `;
        
        return tableHTML;
    }

    // Escape HTML to prevent XSS
    function escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, function(m) { return map[m]; });
    }

    // Enhanced rendering functions for different response types with large dataset support
    function renderSymptomAnalysis(response) {
        renderBotMessage(response.message);
        if (response.next_action === 'hospital_comparison' && response.location) {
            setTimeout(() => {
                renderBotMessage('🔍 Searching through 4,000+ hospitals nationwide for the best prices...');
                compareHospitalPrices(response.procedures.join(' '), response.location);
            }, 2000);
        }
    }
    
    function renderPriceComparison(response) {
        if (response.hospitals && response.hospitals.length > 0) {
            renderHospitalComparison(response.hospitals, response.procedures);
        } else {
            renderBotMessage(response.message);
        }
    }
    
    function renderDetailedComparison(response) {
        if (response.hospitals && response.hospitals.length > 0) {
            renderHospitalComparison(response.hospitals, response.procedures);
        } else {
            renderBotMessage(response.message);
        }
    }
    
    function renderHospitalList(response) {
        renderBotMessage(response.message);
    }
    
    function renderInsuranceDetails(response) {
        renderBotMessage(response.message);
    }
    
    function renderProcedureInfo(response) {
        renderBotMessage(response.message);
    }
    
    function renderEmergencyInfo(response) {
        const emergencyMessage = response.message.replace('🚨', '🚨');
        renderBotMessage(emergencyMessage);
    }
    
    function renderGeneralAssistance(response) {
        renderBotMessage(response.message);
        if (response.suggestions) {
            renderSuggestions(response.suggestions);
        }
    }
    
    function renderSuggestions(suggestions) {
        const suggestionsElement = document.createElement('div');
        suggestionsElement.className = 'message bot-message';
        
        let suggestionsHTML = `
            <div class="message-avatar">💡</div>
            <div class="message-content">
                <p><strong>Quick suggestions:</strong></p>
                <div class="suggestions-container">
        `;
        
        suggestions.forEach(suggestion => {
            suggestionsHTML += `
                <button class="suggestion-btn" onclick="sendQuickMessage('${suggestion}')">
                    ${suggestion}
                </button>
            `;
        });
        
        suggestionsHTML += `
                </div>
            </div>
        `;
        
        suggestionsElement.innerHTML = suggestionsHTML;
        chatMessages.appendChild(suggestionsElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Render bot message with dynamic typing
    function renderBotMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message bot-message';
        
        const contentElement = document.createElement('div');
        contentElement.className = 'message-content';
        
        const textElement = document.createElement('p');
        contentElement.appendChild(textElement);
        
        messageElement.innerHTML = `
            <div class="message-avatar">🤖</div>
        `;
        messageElement.appendChild(contentElement);
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Dynamic typing effect
        typeMessage(textElement, message);
    }
    
    // Render bot message with table (no typing for tables)
    function renderBotMessageWithTable(message, tableHTML) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message bot-message';
        
        messageElement.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="message-content">
                <p>${message}</p>
                ${tableHTML}
            </div>
        `;
        
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Dynamic typing effect
    function typeMessage(element, message) {
        let index = 0;
        const speed = 30; // Typing speed in milliseconds
        
        function typeWriter() {
            if (index < message.length) {
                element.innerHTML += message.charAt(index);
                index++;
                setTimeout(typeWriter, speed);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        }
        
        typeWriter();
    }

    // Show loading
    function showLoading() {
        loadingIndicator.classList.add('show');
    }

    // Hide loading
    function hideLoading() {
        loadingIndicator.classList.remove('show');
    }

    // Quick message actions
    window.sendQuickMessage = (message) => {
        chatInput.value = message;
        sendMessage();
    };
    
    // Request procedure location
    window.requestProcedureLocation = (procedure) => {
        renderUserMessage(`I need ${procedure} pricing information`);
        
        // Show loading
        showLoading();
        
        // Show location request
        const locationMessage = `I can help you find the best ${procedure} prices! To give you accurate pricing in your area, please tell me:\n\n📍 **Your City and State**\n\nFor example:\n• "Dallas, Texas"\n• "Chicago, Illinois"\n• "Los Angeles, California"\n• "Lubbock, Texas"\n\nWhich city are you in?`;
        
        setTimeout(() => {
            hideLoading();
            renderBotMessage(locationMessage);
        }, 1000);
    };
    
    // Request insurance comparison form
    window.requestInsuranceComparison = () => {
        renderUserMessage('I need insurance comparison help');
        
        // Show loading
        showLoading();
        
        const insuranceFormMessage = `🏥 **Insurance Comparison - Please Provide Details**\n\nTo give you the most accurate insurance comparison, I need:\n\n📋 **Insurance Plan:** (e.g., UnitedHealthcare, Aetna, Blue Cross Blue Shield)\n📍 **State:** (e.g., Texas, California, New York)\n🏙️ **City:** (e.g., Dallas, Los Angeles, Chicago)\n📮 **ZIP Code:** (optional, for precise local rates)\n\n**Available Insurance Plans:**\n• UnitedHealthcare - Nationwide\n• Anthem Blue Cross Blue Shield - 14 states + DC\n• Aetna - Nationwide\n• Cigna - Nationwide\n• Humana - Nationwide\n• Kaiser Permanente - 8 states + DC\n• Medicare - Nationwide\n• Medicaid - All states\n\n💡 **Example:** 'I have UnitedHealthcare in Dallas, Texas 75201'\nor 'Compare Aetna insurance in Chicago IL'`;
        
        setTimeout(() => {
            hideLoading();
            renderBotMessage(insuranceFormMessage);
        }, 1000);
    };
    
    // Render professional analysis with enhanced tabular format
    function renderProfessionalAnalysis(response) {
        if (response.display_format === 'table' && response.hospitals && response.hospitals.length > 0) {
            renderProfessionalTable(response);
        } else {
            renderBotMessage(response.message);
        }
    }
    
    function renderProfessionalTable(response) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message bot-message';
        
        // Parse the professional message to extract sections
        const message = response.message;
        const sections = parseProfessionalMessage(message);
        
        let contentHTML = `
            <div class="message-avatar">🤖</div>
            <div class="message-content professional-analysis">
                ${sections.header}
                ${sections.summary}
                ${createProfessionalHospitalTable(response.hospitals, response.procedures)}
                ${sections.procedureBreakdown || ''}
                ${sections.insurance || ''}
                ${sections.actions || ''}
            </div>
        `;
        
        messageElement.innerHTML = contentHTML;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function parseProfessionalMessage(message) {
        const sections = {
            header: '',
            summary: '',
            procedureBreakdown: '',
            insurance: '',
            actions: ''
        };
        
        // Extract header (first few lines)
        const lines = message.split('\n');
        let currentSection = 'header';
        
        for (let i = 0; i < Math.min(5, lines.length); i++) {
            if (lines[i].includes('HEALTHCARE PRICE ANALYSIS') || lines[i].includes('Procedure(s):') || lines[i].includes('Insurance:') || lines[i].includes('Report Date:')) {
                sections.header += `<p>${formatMessageLine(lines[i])}</p>`;
            }
        }
        
        // Extract summary section
        const summaryStart = message.indexOf('EXECUTIVE SUMMARY');
        const summaryEnd = message.indexOf('DETAILED HOSPITAL COMPARISON');
        if (summaryStart !== -1 && summaryEnd !== -1) {
            const summaryText = message.substring(summaryStart, summaryEnd);
            sections.summary = `<div class="summary-section">${formatSummarySection(summaryText)}</div>`;
        }
        
        // Extract insurance section
        const insuranceStart = message.indexOf('INSURANCE IMPACT ANALYSIS');
        const actionsStart = message.indexOf('RECOMMENDED ACTIONS');
        if (insuranceStart !== -1 && actionsStart !== -1) {
            const insuranceText = message.substring(insuranceStart, actionsStart);
            sections.insurance = `<div class="insurance-section">${formatInsuranceSection(insuranceText)}</div>`;
        }
        
        // Extract actions section
        if (actionsStart !== -1) {
            const actionsText = message.substring(actionsStart);
            sections.actions = `<div class="actions-section">${formatActionsSection(actionsText)}</div>`;
        }
        
        return sections;
    }
    
    function formatMessageLine(line) {
        return line
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/🏥|📋|🛡️|📅/g, (match) => `<span class="emoji">${match}</span>`);
    }
    
    function formatSummarySection(text) {
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/🏆|💰|💸|💡/g, (match) => `<span class="emoji">${match}</span>`)
            .replace(/\n/g, '<br>');
    }
    
    function formatInsuranceSection(text) {
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/🛡️|✅|📞/g, (match) => `<span class="emoji">${match}</span>`)
            .replace(/\n/g, '<br>');
    }
    
    function formatActionsSection(text) {
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/🎯|1️⃣|2️⃣|3️⃣|4️⃣|📞|📍|❓/g, (match) => `<span class="emoji">${match}</span>`)
            .replace(/\n/g, '<br>');
    }
    
    function createProfessionalHospitalTable(hospitals, procedures) {
        let tableHTML = `
            <div class="professional-table-container">
                <h4>🏥 Hospital Comparison Results</h4>
                <table class="professional-data-table">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Hospital Name</th>
                            <th>Cash Price</th>
                            <th>Rating</th>
                            <th>Wait Time</th>
                            <th>Emergency</th>
                            <th>Contact</th>
                        </tr>
                    </thead>
                    <tbody>
        `;
        
        hospitals.slice(0, 5).forEach((hospitalData, index) => {
            const hospital = hospitalData.hospital;
            const rank = index + 1;
            const name = hospital.name.length > 25 ? hospital.name.substring(0, 22) + '...' : hospital.name;
            const price = `$${hospitalData.total_cash_cost.toLocaleString()}`;
            const rating = `⭐ ${hospital.rating}`;
            const waitTime = `${hospital.average_wait_time}min`;
            const emergency = hospital.emergency ? '🚨 YES' : '❌ NO';
            const phone = hospital.phone;
            
            const rowClass = index === 0 ? 'best-option' : '';
            
            tableHTML += `
                <tr class="${rowClass}">
                    <td class="rank-cell">${rank}</td>
                    <td class="hospital-cell">
                        <div class="hospital-name">${name}</div>
                        <div class="hospital-address">${hospital.address}</div>
                    </td>
                    <td class="price-cell">${price}</td>
                    <td class="rating-cell">${rating}</td>
                    <td class="wait-cell">${waitTime}</td>
                    <td class="emergency-cell">${emergency}</td>
                    <td class="contact-cell">
                        <a href="tel:${phone}" class="phone-link">📞 ${phone}</a>
                    </td>
                </tr>
            `;
        });
        
        tableHTML += `
                    </tbody>
                </table>
        `;
        
        // Add procedure breakdown for the best hospital
        if (hospitals[0].procedures && hospitals[0].procedures.length > 0) {
            const bestHospital = hospitals[0];
            tableHTML += `
                <div class="procedure-breakdown">
                    <h5>💊 Procedure Breakdown - ${bestHospital.hospital.name}</h5>
                    <table class="procedure-table">
                        <thead>
                            <tr>
                                <th>Procedure</th>
                                <th>Base Price</th>
                                <th>Cash Price</th>
                                <th>Savings</th>
                            </tr>
                        </thead>
                        <tbody>
            `;
            
            bestHospital.procedures.forEach(proc => {
                tableHTML += `
                    <tr>
                        <td>${proc.procedure}</td>
                        <td>$${proc.base_price.toLocaleString()}</td>
                        <td class="price-cell">$${proc.cash_price.toLocaleString()}</td>
                        <td class="savings-cell">$${proc.savings_cash.toLocaleString()}</td>
                    </tr>
                `;
            });
            
            tableHTML += `
                        </tbody>
                    </table>
                </div>
            `;
        }
        
        // Add summary info
        const cheapest = hospitals[0];
        const mostExpensive = hospitals[hospitals.length - 1];
        const totalSavings = mostExpensive.total_cash_cost - cheapest.total_cash_cost;
        
        tableHTML += `
                <div class="table-summary">
                    <div class="summary-item">
                        <span class="label">💡 Best Value:</span>
                        <span class="value">${cheapest.hospital.name} - $${cheapest.total_cash_cost.toLocaleString()}</span>
                    </div>
                    <div class="summary-item">
                        <span class="label">💰 Potential Savings:</span>
                        <span class="value savings">Up to $${totalSavings.toLocaleString()}</span>
                    </div>
                </div>
            </div>
        `;
        
        return tableHTML;
    }
    
    // Enhanced rendering functions for new response types
    function renderProcedureLocationRequest(response) {
        renderBotMessage(response.message);
    }
    
    function renderProcedureLocationAnalysis(response) {
        renderBotMessage(response.message);
        if (response.hospitals && response.hospitals.length > 0) {
            setTimeout(() => {
                renderHospitalComparison(response.hospitals, response.procedures);
            }, 1500);
        }
    }
    
    function renderInsuranceFormRequest(response) {
        renderBotMessage(response.message);
    }
    
    function renderInsuranceLocationRequest(response) {
        renderBotMessage(response.message);
    }
    
    function renderInsuranceLocationAnalysis(response) {
        renderBotMessage(response.message);
        
        // If there are network hospitals, show them in a simple table
        if (response.network_hospitals && response.network_hospitals.length > 0) {
            setTimeout(() => {
                const hospitalsTable = createNetworkHospitalsTable(response.network_hospitals, response.location);
                renderBotMessageWithTable(`🏥 **In-Network Hospitals in ${response.location}:**`, hospitalsTable);
            }, 1500);
        }
    }
    
    function createNetworkHospitalsTable(hospitals, location) {
        let tableHTML = `
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Hospital Name</th>
                        <th>Rating</th>
                        <th>Phone</th>
                        <th>Emergency</th>
                        <th>Address</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        hospitals.slice(0, 8).forEach((hospital, index) => {
            const emergency = hospital.emergency ? '✅ Yes' : '❌ No';
            
            tableHTML += `
                <tr>
                    <td><strong>${hospital.name}</strong></td>
                    <td class="rating-cell">⭐ ${hospital.rating}/5</td>
                    <td>📞 ${hospital.phone}</td>
                    <td>${emergency}</td>
                    <td><small>${hospital.address}</small></td>
                </tr>
            `;
        });
        
        tableHTML += `
                </tbody>
            </table>
            <div style="margin-top: 1rem; padding: 0.75rem; background: rgba(255,255,255,0.05); border-radius: 0.5rem;">
                💡 <strong>Tip:</strong> Call ahead to verify network participation and get current pricing.
            </div>
        `;
        
        return tableHTML;
    }

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});

