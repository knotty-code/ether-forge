/*
Copyright 2025.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package v1alpha1

// CircuitGenieStateSpec defines the desired state of CircuitGenieState
type CircuitGenieStateSpec struct {
	// +eda:ui:title="Nodes"
	// List of TopoNodes this login banner has been applied to
	Nodes []string `json:"nodes,omitempty"`
	// +eda:ui:title="Subnets"
	// List of nodes this banner has been applied to
	Subnets []string `json:"subnets,omitempty"`
}

// CircuitGenieStateStatus defines the observed state of CircuitGenieState
type CircuitGenieStateStatus struct {
}
