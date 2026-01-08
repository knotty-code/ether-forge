/*
Copyright 2026.

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

// LinkAppSpec defines the desired state of LinkApp
type LinkAppSpec struct {
	// +kubebuilder:validation:Optional
	// +eda:ui:columnspan=2
	// +eda:ui:orderpriority=100
	// +eda:ui:autocomplete=`{"group":"interfaces.eda.nokia.com", "version":"v1alpha1", "resource":"interfaces"}`
	// +eda:ui:title="Local Interface"
	LocalInterface string `json:"local,omitempty"`
	// +kubebuilder:validation:Optional
	// +eda:ui:columnspan=2
	// +eda:ui:orderpriority=100
	// +eda:ui:autocomplete=`{"group":"interfaces.eda.nokia.com", "version":"v1alpha1", "resource":"interfaces"}`
	// +eda:ui:title="Remote Interface"
	RemoteInterface string `json:"remote,omitempty"`
}

// LinkAppStatus defines the observed state of LinkApp
type LinkAppStatus struct {
}
